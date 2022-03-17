from flask_sqlalchemy import SQLAlchemy, BaseQuery
from pytest import fixture
from sqlalchemy import String, Integer

from app.common.search import sort_query
from app.test.fixtures import app, db


@fixture
def query(db: SQLAlchemy):
    class DummyModel(db.Model):
        id = db.Column(Integer, primary_key=True, autoincrement=True)
        field_1 = db.Column(String(10),)

    return DummyModel.query


def test_sort_query(query: BaseQuery):
    # Test existing field, default direction
    query_1 = sort_query(query, field="field_1")
    assert query != query_1
    assert "ORDER BY core.dummy_model.field_1 ASC" in str(query_1.statement)

    # Test existing field, desc direction
    query_2 = sort_query(query, field="field_1", direction="desc")
    assert query_1 != query_2
    assert "ORDER BY core.dummy_model.field_1 DESC" in str(query_2.statement)

    # Test unknown field
    query_3 = sort_query(query, field="field_unknown")
    assert query == query_3
