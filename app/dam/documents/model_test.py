from flask_sqlalchemy import SQLAlchemy

from app.dam.documents import Document

# FIXTURES IMPORT
from app.test.fixtures import app, db

# from .test.fixtures import document


def test_document_create(document: Document):
    assert document


def test_document_retrieve(document: Document, db: SQLAlchemy):
    db.session.add(document)
    db.session.commit()
    s = Document.query.first()
    assert s.__dict__ == document.__dict__


def test_document_update(document: Document, db: SQLAlchemy):
    db.session.add(document)
    db.session.commit()
    document.name = "Chèque en blanc"
    db.session.add(document)
    db.session.commit()

    res = Document.query.get(document.id)

    assert res.name == "Chèque en blanc"
    assert res.updated_at is not None
