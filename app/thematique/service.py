from flask import current_app
from app.auth.users.model import User

from app.building import Building
from app.common.firestore_utils import FirestoreUtils
from app.lot import Lot
from app.thematique.config import THEMATICS
from app.thematique.error_handlers import (
    VersionNotFoundException,
    InvalidScopeException,
    InvalidResourceIdException,
    MissingVersionIdException,
    MissingStepIdException,
    UnauthorizedToDeleteException,
    UnauthorizedToUpdateException,
    UnauthorizedDuplicationException,
    NotUniqueDataAndNameVersionException
)
from app.thematique.model import ThematiqueMission
from app.thematique.schema import StepSchema, VersionSchema
from app import db


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
        if version.exists:
            version_dict = version.to_dict()
            version_dict["id"] = version.id
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

        # cast to int in case it is a str
        resource_id = int(resource_id)
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

        # If scope is one of specified child in mapping_model
        # then inherit parent's version into child
        mapping_model = {"lot": Lot, "building": Building}
        if scope in mapping_model.keys():
            if ThematiqueService.check_inheritance_authorization(
                scope, thematique_name, firestore_service
            ):
                list_docs = ThematiqueService.handle_child(
                    scope=scope,
                    child_model=mapping_model[scope],
                    child_id=resource_id,
                    thematique_name=thematique_name,
                    firestore_utils=firestore_service,
                    list_docs=list_docs,
                )
        return sorted(list_docs, key=lambda d: d["version_date"], reverse=True)

    @staticmethod
    def duplicate_thematique(version):
        firestore_service = FirestoreUtils()
        ThematiqueService.check_duplication_authorization(version, firestore_service)

        collection = firestore_service.client.collection(current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION"))

        unique_date_and_name = ThematiqueService.check_date_and_name_version(collection, version)
        if not unique_date_and_name:
            raise NotUniqueDataAndNameVersionException
        
        steps = version.get("steps", [])
        del version["steps"]
        if "id" in version:
            del version["id"]
        document = collection.document()
        document.set(version)

        for s in steps:
            step_doc = document.collection(
                current_app.config.get("FIRESTORE_STEPS_COLLECTION")
            ).document()
            step_doc.set(s)

        return ThematiqueService.get_version(document.id)

    @staticmethod
    def check_duplication_authorization(version, firestore_service):
        # Get templates collection
        template = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_TEMPLATE_COLLECTION")
            )
            .where("label", "==", version.get("label"))
            .where("scope", "==", version.get("scope"))
            .where("versionnable", "==", True)
            .get()
        )

        # Found template with correct label, scope and versionnable attr
        if len(template) == 0:
            raise UnauthorizedDuplicationException

    @staticmethod
    def check_inheritance_authorization(scope, thematic_name, firestore_service):
        # Get templates collection
        template = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_TEMPLATE_COLLECTION")
            )
            .where("thematique_name", "==", thematic_name)
            .where("scope", "==", scope)
            .where("heritable", "==", True)
            .get()
        )
        # Found template with correct thematic_name, scope and heritable attr
        return len(template) > 0

    def check_date_and_name_version(collection, version_to_duplicate):
        docs = collection.stream()
        for doc in docs:
            obj = doc.to_dict()
            if obj.get('version_name') == version_to_duplicate.get('version_name') and \
               obj.get('version_date') == version_to_duplicate.get('version_date') and \
               obj.get('scope') == version_to_duplicate.get('scope'):
                return False
        return True

    @staticmethod
    def update_step(version_id: str, step_id: str, payload: StepSchema, user: User):

        if version_id in ["", None]:
            raise MissingVersionIdException
        if step_id in ["", None]:
            raise MissingStepIdException

        firestore_service = FirestoreUtils()
        step = firestore_service.get_step_by_id(version_id=version_id, step_id=step_id)

        for key in ["legendes", "name", "order", "id"]:
            if key in payload["metadata"]:
                del payload["metadata"][key]

        from app.thematique.historics.service import HistoricService
        new_attrs = {
            "thematique_id": version_id,
            "updated_by": user
        }
        old_status = step.to_dict()["metadata"]["status"]
        new_status = payload["metadata"]["status"]
        if old_status != new_status:
            new_attrs["status_changed"]= True,
            new_attrs["old_status"] = old_status,
            new_attrs["new_status"]= new_status
        else:
            new_attrs["status_changed"]= False

        step.reference.set(payload, merge=True)

        HistoricService.create(new_attrs, commit=True)
        return ThematiqueService.get_version(version_id)

    @staticmethod
    def update_version(version_id: str, payload: VersionSchema):

        if version_id in ["", None]:
            raise MissingVersionIdException

        firestore_service = FirestoreUtils()

        version = firestore_service.get_version_by_id(version_id=version_id)
        version = version.to_dict()
        if version.get('versionnable', None) and version.get('heritable', None):
            # Only update from copro scope if heritable
            if version.get("scope") != "copro":
                raise UnauthorizedToUpdateException
            # Get versions with same name and date (unicity checked on create)
            matching_versions = firestore_service.query_version(
                version_name=version.get('version_name'),
                version_date=version.get('version_date'),
                thematique_name=version.get('thematique_name')
            )
            # Update all inherited versions with the same version_name and version_date
            for vers in matching_versions:
                vers.reference.set(payload, merge=True)

        elif version.get('versionnable', None):
            # Simply update version when only versionnable
            version.reference.set(payload, merge=True)
        else:
            # Nothing to update if not versionnable (should not happend)
            raise UnauthorizedToUpdateException

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
    def handle_child(
        scope,
        child_model,
        child_id,
        thematique_name,
        firestore_utils: FirestoreUtils,
        list_docs,
    ):
        db_object = child_model.query.get(child_id)
        if not db_object:
            raise
        copro_id = db_object.copro_id
        docs = firestore_utils.query_version(
            scope="copro", thematique_name=thematique_name, resource_id=copro_id
        )
        for doc in docs:
            doc_found = False
            for child_doc in list_docs:
                if child_doc.get("version_date") == doc.get(
                    "version_date"
                ) and child_doc.get("version_name") == doc.get("version_name"):
                    doc_found = True
                    break
            if not doc_found:
                template = ThematiqueService.list_templates(
                    scope=scope, name=doc.get("thematique_name")
                )
                if len(template) == 0:
                    raise
                template = template[0]
                template["version_name"] = doc.get("version_name")
                template["version_date"] = doc.get("version_date")
                template["resource_id"] = int(child_id)
                version_created = ThematiqueService.duplicate_thematique(template)
                list_docs.append(version_created)
        return list_docs

    @staticmethod
    def delete_copro_version(version_id):
        """
        Delete a copro version of a thematic, with versions of same thematic, version name and date for its buildings and lots
        """
        version = ThematiqueService.get_version(version_id)
        if version.get("scope") != "copro":
            raise UnauthorizedToDeleteException
        ThematiqueService.delete_sub_versions(
            copro_id=version.get("resource_id"),
            thematique_name=version.get("thematique_name"),
            version_name=version.get("version_name"),
            version_date=version.get("version_date"),
        )
        ThematiqueService.delete_version(version_id)

    @staticmethod
    def delete_version(version_id, firestore_service=None):
        """
        Delete a specified version and its steps
        """
        if not firestore_service:
            firestore_service = FirestoreUtils()
        version = firestore_service.get_version_by_id(version_id)
        if not version.exists:
            raise VersionNotFoundException
        steps = version.reference.collection(
            current_app.config.get("FIRESTORE_STEPS_COLLECTION")
        ).get()
        for step in steps:
            step.reference.delete()
        version.reference.delete()

    @staticmethod
    def delete_sub_versions(copro_id, thematique_name, version_name, version_date):
        """
        Delete versions with same thematic, name and date for sub items of a copro
        """
        # fetch building ids of copro
        buildings = (
            Building.query.with_entities(Building.id)
            .filter(Building.copro_id == copro_id)
            .all()
        )
        # fetch lot ids of copro
        lots = Lot.query.with_entities(Lot.id).filter(Lot.copro_id == copro_id).all()
        firestore_service = FirestoreUtils()
        # fetch all versions of same name, version name and date
        documents = firestore_service.query_version(
            thematique_name=thematique_name,
            version_name=version_name,
            version_date=version_date,
        )
        for d in documents:
            doc_dict = d.to_dict()
            if (
                doc_dict.get("scope") == "building"
                and (doc_dict.get("resource_id"),) in buildings
            ):
                ThematiqueService.delete_version(
                    d.id, firestore_service=firestore_service
                )
            if (
                doc_dict.get("scope") == "lot"
                and (doc_dict.get("resource_id"),) in lots
            ):
                ThematiqueService.delete_version(
                    d.id, firestore_service=firestore_service
                )

    @staticmethod
    def init_mission_thematics(mission_id):
        for t in THEMATICS:
            tm = ThematiqueMission(
                **{"mission_id": mission_id, "thematique_name": t, "authorized": True}
            )
            db.session.add(tm)
            db.session.commit()
