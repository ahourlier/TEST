from flask import current_app, jsonify

from app.building import Building
from app.common.firestore_utils import FirestoreUtils
from app.lot import Lot
from app.thematique.exceptions import (
    VersionNotFoundException,
    InvalidScopeException,
    InvalidResourceIdException,
    MissingVersionIdException,
    MissingStepIdException,
)
from app.thematique.schema import StepSchema


class ThematiqueService:
    @staticmethod
    def list_templates(scope=None, name=None):
        thematiques = []
        thematiques_added = []
        firestore_service = FirestoreUtils()
        all_templates_query = firestore_service.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_TEMPLATE_COLLECTION")
        )
        if scope and scope != "mission":
            all_templates_query = all_templates_query.where("scope", "==", scope)

        if name:
            all_templates_query = all_templates_query.where(
                "thematique_name", "==", name
            )

        for doc in all_templates_query.get():
            to_dict = doc.to_dict()
            to_dict["id"] = doc.id

            if scope == "mission":
                if to_dict.get("thematique_name") not in thematiques_added:
                    thematiques_added.append(to_dict.get("thematique_name"))
                    # del to_dict["scope"]
                    # del to_dict["legendes"]
                else:
                    continue
            else:
                to_dict["steps"] = ThematiqueService.handle_steps(doc)
            thematiques.append(to_dict)

        return thematiques

    @staticmethod
    def handle_steps(doc, copy_ids=False):
        steps = doc.reference.collection(
            current_app.config.get("FIRESTORE_STEPS_COLLECTION")
        ).get()
        step_list = []
        for s in steps:
            s_obj = s.to_dict()
            if copy_ids:
                s_obj["metadata"]["id"] = s.id
            step_list.append(s_obj)
        return step_list

    @staticmethod
    def get_version(version_id):
        firestore_service = FirestoreUtils()
        version = firestore_service.get_version_by_id(version_id)
        if version:
            version_dict = version.to_dict()
            version_dict["steps"] = ThematiqueService.handle_steps(
                version, copy_ids=True
            )
            return version_dict
        raise VersionNotFoundException

    @staticmethod
    def list_versions(scope, resource_id, thematique_name):

        if scope in ["", None]:
            raise InvalidScopeException
        if resource_id in ["", None]:
            raise InvalidResourceIdException

        firestore_service = FirestoreUtils()
        documents = firestore_service.query_version(
            scope=scope, resource_id=resource_id, thematique_name=thematique_name
        )

        list_docs = []
        for doc in documents:
            doc_dict = doc.to_dict()
            doc_dict["id"] = doc.id
            doc_dict["steps"] = ThematiqueService.handle_steps(doc, copy_ids=True)
            list_docs.append(doc_dict)

        return list_docs

    @staticmethod
    def duplicate_thematique(version):
        firestore_service = FirestoreUtils()
        steps = version.get("steps", [])
        del version["steps"]
        if "id" in version:
            del version["id"]
        document = firestore_service.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
        ).document()
        document.set(version)

        for s in steps:
            step_doc = document.collection(
                current_app.config.get("FIRESTORE_STEPS_COLLECTION")
            ).document()
            step_doc.set(s)

        mapping_model = {"lot": Lot, "building": Building}

        if version.get("scope") in mapping_model.keys():
            ThematiqueService.handle_parent(
                version=version,
                model_object=mapping_model[version.get("scope")].query.get(
                    version.get("resource_id")
                ),
                firestore_service=firestore_service,
            )

        return ThematiqueService.get_version(document.id)

    @staticmethod
    def update_step(version_id: str, step_id: str, payload: StepSchema):

        if version_id in ["", None]:
            raise MissingVersionIdException
        if step_id in ["", None]:
            raise MissingStepIdException

        firestore_service = FirestoreUtils()
        step = firestore_service.get_step_by_id(version_id=version_id, step_id=step_id)

        for key in ["legendes", "name", "order", "id"]:
            if key in payload["metadata"]:
                del payload["metadata"][key]

        step.set(payload, merge=True)
        return ThematiqueService.get_version(version_id)

    @staticmethod
    def get_thematiques_from_mission(mission_id):
        # todo changed with fetching ThematiqueMission for mission_id
        return [
            {
                "mision_id": mission_id,
                "thematique_name": "SUIVI_FINANCEMENT",
                "authorized": True,
            }
        ]

    @staticmethod
    def handle_parent(version, model_object, firestore_service: FirestoreUtils):
        if not model_object:
            raise
        copro_id = model_object.copro.id
        copro_version = firestore_service.query_version(
            thematique_name=version.get("thematique_name"),
            scope="copro",
            resource_id=copro_id,
            version_date=version.get("version_date"),
            version_name=version.get("version_name"),
        )
        if len(copro_version) == 0:
            template = ThematiqueService.list_templates(
                "copro", version.get("thematique_name")
            )
            if len(template) == 0:
                raise
            template = template[0]
            template["version_name"] = version.get("version_name")
            template["version_date"] = version.get("version_date")
            template["resource_id"] = copro_id
            ThematiqueService.duplicate_thematique(template)
        return