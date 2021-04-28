from flask_sqlalchemy import Pagination
from pytest import fixture

from app.common.schemas import PaginatedSchema


@fixture
def paginated_schema() -> PaginatedSchema:
    return PaginatedSchema()


def test_agency_schema_create(paginated_schema: PaginatedSchema):
    assert paginated_schema


def test_agency_schema_ok(paginated_schema: PaginatedSchema):
    params = {
        "page": 1,
        "per_page": 20,
        "total": 10,
    }

    paginated_object = Pagination(query=None, items=None, **params)
    schema = paginated_schema.dump(paginated_object)

    assert schema.get("pageSize") == 20
    assert schema.get("totalItems") == 10
    assert schema.get("page") == 1
