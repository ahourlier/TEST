import base64
from flask import g
from typing import List
from flask_sqlalchemy import Pagination
from sqlalchemy import or_, and_, func

from app import db
from app.auth.users.model import User, UserRole
from app.auth.users.service import UserService
from app.building.service import BuildingService
from app.cle_repartition.service import CleRepartitionService
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.app_name import App
from app.common.drive_utils import DriveUtils
from app.common.exceptions import EnumException
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.common.db_utils import DBUtils
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.architect.model import Architect
from app.copro.architect.service import ArchitectService
from app.copro.cadastre import Cadastre
from app.copro.caretaker.model import CareTaker
from app.copro.caretaker.service import CareTakerService
from app.copro.copros.error_handlers import (
    CoproNotFoundException,
    MissionNotTypeCoproException,
    EnumException as CoproEnumException,
)
from app.copro.copros.interface import CoproInterface
from app.copro.copros.model import Copro
from app.copro.employee.model import Employee
from app.copro.employee.service import EmployeeService
from app.copro.fire_safety_personnel.model import FireSafetyPersonnel
from app.copro.fire_safety_personnel.service import FireSafetyPersonnelService
from app.copro.moe.model import Moe
from app.copro.moe.service import MoeService
from app.copro.president import President
from app.auth.users import User
from app.copro.president.service import PresidentService
from app.copro.syndic.service import SyndicService
from app.mission.missions.service import MissionService
from app.thematique.service import ThematiqueService

from app.building.settings import NB_LOOP_ACCESS_CODE

COPRO_DEFAULT_PAGE = 1
COPRO_DEFAULT_PAGE_SIZE = 20
COPRO_DEFAULT_SORT_FIELD = "created_at"
COPRO_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "copro_type": {"enum_key": "CoproType"},
    "construction_time": {"enum_key": "CoproConstructionTime"},
}

MODEL_MAPPING = {"address_1": Address, "address": Address, "user_in_charge": User}


class CoproService:
    @staticmethod
    def get_all(
        page=COPRO_DEFAULT_PAGE,
        size=COPRO_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=COPRO_DEFAULT_SORT_FIELD,
        direction=COPRO_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        cs_id=None,
        user=None,
    ) -> Pagination:
        import app.mission.permissions as mission_permissions
        from app.mission.missions import Mission

        q = Copro.query
        if "." in sort_by:
            q = CoproService.sort_from_sub_model(q, sort_by, direction)
        else:
            q = sort_query(q, sort_by, direction)

        q = q.filter(or_(Copro.is_deleted == False, Copro.is_deleted == None))
        if term is not None:
            search_term = f"%{term}%"
            q = q.join(
                Address,
                or_(Copro.address_1_id == Address.id, Copro.address_2_id == Address.id),
            ).filter(
                or_(
                    Copro.name.ilike(search_term),
                    Address.full_address.ilike(search_term),
                )
            )

        if mission_id is not None:
            q = q.filter(Copro.mission_id == mission_id)

        if cs_id is not None:
            q = q.filter(Copro.cs_id == cs_id)

        if user is not None and user.role != UserRole.ADMIN:
            q = q.join(Mission)
            q = mission_permissions.MissionPermission.filter_query_mission_by_user_permissions(
                q, user
            )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: CoproInterface) -> Copro:

        try:
            ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        except EnumException as e:
            raise CoproEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        mission = MissionService.get_by_id(new_attrs.get("mission_id"))
        if mission.mission_type != App.COPRO:
            raise MissionNotTypeCoproException

        if new_attrs.get("access_code"):
            new_attrs["access_code"] = BuildingService.encode_access_code(
                new_attrs.get("access_code")
            )

        if new_attrs.get("address_1"):
            new_attrs["address_1_id"] = AddressService.create_address(
                new_attrs.get("address_1")
            )
            del new_attrs["address_1"]

        if new_attrs.get("address_2"):
            new_attrs["address_2_id"] = AddressService.create_address(
                new_attrs.get("address_2")
            )
            del new_attrs["address_2"]

        if new_attrs.get("syndic_manager_address"):
            new_attrs["syndic_manager_address_id"] = AddressService.create_address(
                new_attrs.get("syndic_manager_address")
            )
            del new_attrs["syndic_manager_address"]

        if new_attrs.get("admin_manager_address"):
            new_attrs["admin_manager_address_id"] = AddressService.create_address(
                new_attrs.get("admin_manager_address")
            )
            del new_attrs["admin_manager_address"]

        phones = []
        if "syndic_manager_phone_number" in new_attrs:
            if new_attrs.get("syndic_manager_phone_number", None):
                phones.append(
                    PhoneNumber(**new_attrs.get("syndic_manager_phone_number"))
                )
            del new_attrs["syndic_manager_phone_number"]
        if "admin_manager_phone_number" in new_attrs:
            if new_attrs.get("admin_manager_phone_number", None):
                phones.append(
                    PhoneNumber(**new_attrs.get("admin_manager_phone_number"))
                )
            del new_attrs["admin_manager_phone_number"]
        new_attrs["phones"] = phones

        cadastres = None
        if new_attrs.get("cadastres"):
            cadastres = new_attrs.get("cadastres")
            del new_attrs["cadastres"]

        if new_attrs.get("moe"):
            new_attrs["moe_id"] = MoeService.create(new_attrs.get("moe"))
            del new_attrs["moe"]

        if new_attrs.get("architect"):
            new_attrs["architect_id"] = ArchitectService.create(
                new_attrs.get("architect")
            )
            del new_attrs["architect"]

        if new_attrs.get("caretaker"):
            new_attrs["caretaker_id"] = CareTakerService.create(
                new_attrs.get("caretaker")
            )
            del new_attrs["caretaker"]

        if new_attrs.get("employee"):
            new_attrs["employee_id"] = EmployeeService.create(new_attrs.get("employee"))
            del new_attrs["employee"]

        if new_attrs.get("fire_safety_personnel"):
            new_attrs["fire_safety_personnel_id"] = FireSafetyPersonnelService.create(
                new_attrs.get("fire_safety_personnel")
            )
            del new_attrs["fire_safety_personnel"]

        new_attrs["president_id"] = PresidentService.create(
            new_attrs.get("president", {})
        )
        if new_attrs.get("president"):
            del new_attrs["president"]

        cles_repartition = None
        if "cles_repartition" in new_attrs:
            cles_repartition = new_attrs.get("cles_repartition")
            del new_attrs["cles_repartition"]

        if "urbanis_collaborators" in new_attrs:
            new_attrs["urbanis_collaborators"] = CoproService.handle_collaborators(
                new_attrs.get("urbanis_collaborators", [])
            )

        try:
            new_copro = Copro(**new_attrs)
            db.session.add(new_copro)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise (e)

        if cadastres:
            for c in cadastres:
                c["copro_id"] = new_copro.id
                new_cadastre = Cadastre(**c)
                db.session.add(new_cadastre)
                db.session.commit()

        if cles_repartition:
            CleRepartitionService.handle_keys(new_copro.id, cles_repartition)

        CoproService.create_copro_drive_structure_and_link(new_copro, mission)
        db.session.commit()
        return new_copro

    @staticmethod
    def get(copro_id) -> Copro:
        db_copro = (
            Copro.query.filter(Copro.id == copro_id)
            .filter(Copro.is_deleted == False)
            .first()
        )

        if db_copro is None:
            raise CoproNotFoundException

        return db_copro

    @staticmethod
    def update(db_copro: Copro, changes: CoproInterface, copro_id: int) -> Copro:

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise CoproEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        if "president" in changes:
            if changes.get("president"):
                PresidentService.update(
                    President.query.get(db_copro.president_id), changes.get("president")
                )
            del changes["president"]
            del changes["president_id"]

        if "cadastres" in changes:
            if changes.get("cadastres"):
                delete_cadastres = Cadastre.__table__.delete().where(
                    Cadastre.copro_id == copro_id
                )
                db.session.execute(delete_cadastres)
                db.session.commit()

                for c in changes.get("cadastres"):
                    c["copro_id"] = copro_id
                    new_cadastre = Cadastre(**c)
                    db.session.add(new_cadastre)
                    db.session.commit()

            del changes["cadastres"]

        if "address_1" in changes:
            if changes.get("address_1"):
                if not db_copro.address_1_id:
                    changes["address_1_id"] = AddressService.create_address(
                        changes.get("address_1")
                    )
                else:
                    AddressService.update_address(
                        db_copro.address_1_id, changes.get("address_1")
                    )
            del changes["address_1"]

        if "address_2" in changes:
            if changes.get("address_2"):
                if not db_copro.address_2_id:
                    changes["address_2_id"] = AddressService.create_address(
                        changes.get("address_2")
                    )
                else:
                    AddressService.update_address(
                        db_copro.address_2_id, changes.get("address_2")
                    )
            del changes["address_2"]

        if "syndic_manager_address" in changes:
            if changes.get("syndic_manager_address"):
                if not db_copro.syndic_manager_address:
                    changes[
                        "syndic_manager_address_id"
                    ] = AddressService.create_address(
                        changes.get("syndic_manager_address")
                    )
                else:
                    AddressService.update_address(
                        db_copro.syndic_manager_address_id,
                        changes.get("syndic_manager_address"),
                    )
            del changes["syndic_manager_address"]

        if "admin_manager_address" in changes:
            if changes.get("admin_manager_address"):
                if not db_copro.admin_manager_address:
                    changes["admin_manager_address_id"] = AddressService.create_address(
                        changes.get("admin_manager_address")
                    )
                else:
                    AddressService.update_address(
                        db_copro.admin_manager_address_id,
                        changes.get("admin_manager_address"),
                    )
            del changes["admin_manager_address"]

        # Update phones numbers
        phones = []
        if "syndic_manager_phone_number" in changes:
            if changes["syndic_manager_phone_number"] is not None:
                phones.append(changes.get("syndic_manager_phone_number"))
            del changes["syndic_manager_phone_number"]
        if "admin_manager_phone_number" in changes:
            if changes["admin_manager_phone_number"] is not None:
                phones.append(changes.get("admin_manager_phone_number"))
            del changes["admin_manager_phone_number"]
        PhoneNumberService.update_phone_numbers(db_copro, phones)

        if "user_in_charge" in changes:
            if changes.get("user_in_charge"):
                changes["user_in_charge_id"] = changes.get("user_in_charge").get("id")
            del changes["user_in_charge"]

        if "moe" in changes:
            if changes.get("moe"):
                if not db_copro.moe_id:
                    changes["moe_id"] = MoeService.create(changes.get("moe"))
                else:
                    MoeService.update(
                        Moe.query.get(db_copro.moe_id), changes.get("moe")
                    )
            del changes["moe"]

        if "architect" in changes:
            if changes.get("architect"):
                if not db_copro.architect_id:
                    changes["architect_id"] = ArchitectService.create(
                        changes.get("architect")
                    )
                else:
                    ArchitectService.update(
                        Architect.query.get(db_copro.architect_id),
                        changes.get("architect"),
                    )
            del changes["architect"]

        if "caretaker" in changes:
            if changes.get("caretaker"):
                if not db_copro.caretaker_id:
                    changes["caretaker_id"] = CareTakerService.create(
                        changes.get("caretaker")
                    )
                else:
                    CareTakerService.update(
                        CareTaker.query.get(db_copro.caretaker_id),
                        changes.get("caretaker"),
                    )
            del changes["caretaker"]

        if "employee" in changes:
            if changes.get("employee"):
                if not db_copro.employee_id:
                    changes["employee_id"] = EmployeeService.create(
                        changes.get("employee")
                    )
                else:
                    EmployeeService.update(
                        Employee.query.get(db_copro.employee_id),
                        changes.get("employee"),
                    )
            del changes["employee"]

        if "fire_safety_personnel" in changes:
            if changes.get("fire_safety_personnel"):
                if not db_copro.fire_safety_personnel_id:
                    changes[
                        "fire_safety_personnel_id"
                    ] = FireSafetyPersonnelService.create(
                        changes.get("fire_safety_personnel")
                    )
                else:
                    FireSafetyPersonnelService.update(
                        FireSafetyPersonnel.query.get(
                            db_copro.fire_safety_personnel_id
                        ),
                        changes.get("fire_safety_personnel"),
                    )
            del changes["fire_safety_personnel"]

        if "cles_repartition" in changes:
            CleRepartitionService.handle_keys(
                db_copro.id, changes.get("cles_repartition")
            )
            del changes["cles_repartition"]

        if "access_code" in changes:
            changes["access_code"] = BuildingService.encode_access_code(
                changes.get("access_code")
            )

        if changes.get("urbanis_collaborators") is not None:
            db_copro.urbanis_collaborators = CoproService.handle_collaborators(
                changes.get("urbanis_collaborators", [])
            )
            del changes["urbanis_collaborators"]

        db_copro.update(changes)
        db.session.commit()

        return db_copro

    @staticmethod
    def delete(copro_id: int):
        DBUtils.soft_delete_cascade(copro_id, CoproService)
        return copro_id

    def handle_collaborators(list_dict_collaborators: List[dict]):
        table = []
        for p in list_dict_collaborators:
            table.append(UserService.get(p.get("id")))
        return table

    @staticmethod
    def get_thematiques(copro_id: int):
        copro = CoproService.get(copro_id)
        return ThematiqueService.get_thematiques_from_mission(copro.mission_id)

    @staticmethod
    def search_by_address(address_obj, mission_id):
        try:
            return (
                Copro.query.join(Address, Copro.address_1_id == Address.id)
                .filter(
                    and_(
                        Address.number == str(address_obj.get("number")),
                        func.lower(Address.street)
                        == func.lower(str(address_obj.get("street"))),
                        Address.postal_code == str(address_obj.get("postal_code")),
                        func.lower(Address.city)
                        == func.lower(str(address_obj.get("city"))),
                        Copro.mission_id == mission_id,
                        Copro.is_deleted == False,
                    )
                )
                .first()
            )
        except Exception as e:
            print(e)

    def sort_from_sub_model(query, sort_by, direction):
        values = sort_by.split(".")
        sub_model = MODEL_MAPPING[values[0]]
        sort_by = values[1]
        return sort_query(query, sort_by, direction, sub_model)

    def create_copro_drive_structure_and_link(new_copro, mission):
        folder_name = (
            new_copro.address_1.city
            + " - "
            + new_copro.address_1.number
            + " "
            + new_copro.address_1.street
        )
        copro_folder_id = DriveUtils.create_folder(
            folder_name, mission.sdv2_suivi_animation_folder, g.user.email, None, False
        )
        folders = {
            "T1 - Environnement urbain et cadre de vie": None,
            "T2 - Situation juridique et fonci??re": None,
            "T3 - Occupation sociale": None,
            "T4 - Gestion et fonctionnement": None,
            "T5 - Charges": None,
            "T6 - Impay??s": None,
            "T7 - ??quipements et b??ti": None,
            "T8 - Suivi des financements PC et PPIC": None,
            "T9 - Suivi des financements PP": None,
            "T10 - Positionnement immobilier": None,
        }
        for folder_name in folders:
            folders[folder_name] = DriveUtils.create_folder(
                folder_name, copro_folder_id, g.user.email, None, True
            )
        DriveUtils.batch_request(folders, g.user.email)

        new_copro.sdv2_environement_urbain_folder_id = folders[
            "T1 - Environnement urbain et cadre de vie"
        ]
        new_copro.sdv2_situation_juridique_folder_id = folders[
            "T2 - Situation juridique et fonci??re"
        ]
        new_copro.sdv2_occupation_folder_id = folders["T3 - Occupation sociale"]
        new_copro.sdv2_gestion_folder_id = folders["T4 - Gestion et fonctionnement"]
        new_copro.sdv2_charges_folder_id = folders["T5 - Charges"]
        new_copro.sdv2_impayes_folder_id = folders["T6 - Impay??s"]
        new_copro.sdv2_equipements_folder_id = folders["T7 - ??quipements et b??ti"]
        new_copro.sdv2_suivi_financement_pc_folder_id = folders[
            "T8 - Suivi des financements PC et PPIC"
        ]
        new_copro.sdv2_suivi_financement_pp_folder_id = folders[
            "T9 - Suivi des financements PP"
        ]
        new_copro.sdv2_positionnement_folder_id = folders[
            "T10 - Positionnement immobilier"
        ]
