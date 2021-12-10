from flask import current_app, jsonify

from app.common.firestore_utils import FirestoreUtils
from app.thematique.exceptions import VersionNotFoundException


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
    def list_thematiques(scope, resource_id, thematique_name):
        firestore_service = FirestoreUtils()
        versions = []
        documents = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .where("scope", "==", scope)
            .where("resource_id", "==", resource_id)
            .where("thematique_name", "==", thematique_name)
            .get()
        )
        for d in documents:
            dict_obj = d.to_dict()
            dict_obj["id"] = d.id
            dict_obj["steps"] = ThematiqueService.handle_steps(d, copy_ids=True)
            versions.append(dict_obj)
        return versions

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
        version = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .document(version_id)
            .get()
        )
        if version:
            version_dict = version.to_dict()
            version_dict["steps"] = ThematiqueService.handle_steps(
                version, copy_ids=True
            )
            return version
        raise VersionNotFoundException

    @staticmethod
    def duplicate_thematique(version):
        firestore_service = FirestoreUtils()
        steps = version.get("steps", [])
        del version["steps"]
        document = firestore_service.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
        ).document()
        document.set(version)
        for s in steps:
            step_doc = document.collection(
                current_app.config.get("FIRESTORE_STEPS_COLLECTION")
            ).document()
            step_doc.set(s)
        return ThematiqueService.get_version(document.id)
