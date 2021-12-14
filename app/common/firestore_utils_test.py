from unittest.mock import patch

import pytest
from pytest_mock import mocker
from mockfirestore import MockFirestore

from app.common.firestore_utils import FirestoreUtils


class CurrentAppClass:

    config = {
        "FIRESTORE_THEMATIQUE_COLLECTION": "thematiques",
        "FIRESTORE_STEPS_COLLECTION": "steps",
    }


@pytest.fixture
def firestore_fixture(mocker):
    mock_db = MockFirestore()
    mock_db.collection("users").document("test").set(
        {"email": "testFirestore", "role": "User"}
    )
    mocker.patch("app.common.firestore_utils.current_app", CurrentAppClass())
    mocker.patch("firebase_admin.credentials.Certificate")
    mocker.patch("firebase_admin.initialize_app")
    mocker.patch("firebase_admin.firestore.client", return_value=mock_db)


def test_list_items(firestore_fixture):
    firestore_utils = FirestoreUtils()
    docs = firestore_utils.list_items("users")
    count = count_docs(docs)
    assert count == 1
    firestore_utils.client.collection("users").document("other_test").set(
        {"email": "testFirestore", "role": "User"}
    )
    docs = firestore_utils.list_items("users")
    count = count_docs(docs)
    assert count == 2


def test_query_version(firestore_fixture):
    firestore_utils = FirestoreUtils()
    current_app = CurrentAppClass()
    docs = firestore_utils.query_version(
        thematique_name=None,
        resource_id=None,
        scope=None,
        version_name=None,
        version_date=None,
    )
    count = count_docs(docs)
    assert count == 0
    firestore_utils.client.collection(
        current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
    ).document().set({"thematique_name": "thematique_1"})
    firestore_utils.client.collection(
        current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
    ).document().set({"thematique_name": "thematique_2"})
    docs = firestore_utils.query_version(
        thematique_name=None,
        resource_id=None,
        scope=None,
        version_name=None,
        version_date=None,
    )
    count = count_docs(docs)
    assert count == 2
    docs = firestore_utils.query_version(
        thematique_name="thematique_2",
        resource_id=None,
        scope=None,
        version_name=None,
        version_date=None,
    )
    count = count_docs(docs)
    assert count == 1


def test_version_by_id(firestore_fixture):
    current_app = CurrentAppClass()
    firestore_utils = FirestoreUtils()
    doc = firestore_utils.get_version_by_id("non_existing_document")
    assert doc.to_dict() == {}
    firestore_utils.client.collection(
        current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
    ).document("non_existing_document").set({"existing": True})
    doc = firestore_utils.get_version_by_id("non_existing_document")
    assert doc.to_dict() != {}


def test_get_step_by_id(firestore_fixture):
    current_app = CurrentAppClass()
    firestore_utils = FirestoreUtils()
    step = firestore_utils.get_step_by_id("test", "test_step")
    assert step.to_dict() == {}
    firestore_utils.client.collection(
        current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
    ).document("test").collection(
        current_app.config.get("FIRESTORE_STEPS_COLLECTION")
    ).document(
        "test_step"
    ).set(
        {"existing": True}
    )
    step = firestore_utils.get_step_by_id("test", "test_step")
    assert step.to_dict() != {}


def count_docs(docs):
    cpt = 0
    for _ in docs:
        cpt += 1
    return cpt
