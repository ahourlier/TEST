from copy import copy
from sqlalchemy.sql.elements import and_, or_
from app.building.model import Building
from app.copro.copros.model import Copro

from app.copro.syndic.model import Syndic
from app.combined_structure.model import CombinedStructure
from app.lot.model import Lot
from app.lot.model import LotOwner
from app.person.model import Person


class ComplexFilters:
    @staticmethod
    def build_complex_filters(entity, search_obj):
        """
        Add a key for each complex relation tosearch in (ie. Many to One, Many to Many...)
        """
        complex_filter = {}
        # Copy original search_obj to avoid side effect
        filters_copy = copy(search_obj["filters"])
        for filter in filters_copy:
            # From combined_structure
            if entity == "combined_structure":
                if filter["field"] == "syndic_name":
                    complex_filter[
                        "syndic_name"
                    ] = ComplexFilters.build_syndic_name_query(filter)
                    # Removed because recursiv search couldn't
                    # find this column since it came from another table
                    search_obj["filters"].remove(filter)

            if entity == "building":
                if filter["field"] == "mission_id":
                    complex_filter[
                        "mission_id"
                    ] = ComplexFilters.build_building_mission_id_query(filter)
                    search_obj["filters"].remove(filter)

            if entity == "lot":
                if filter["field"] == "owner_name":
                    complex_filter[
                        "owner_name"
                    ] = ComplexFilters.build_owner_name_query(filter)
                    search_obj["filters"].remove(filter)

                if filter["field"] == "mission_id":
                    complex_filter[
                        "mission_id"
                    ] = ComplexFilters.build_lot_mission_id_query(filter)
                    search_obj["filters"].remove(filter)

        return complex_filter

    @staticmethod
    def build_syndic_name_query(filter):
        """
        Combined Structure: Build query manually when searching by syndic_name
        """
        return (
            Syndic.query.distinct()
            .with_entities(Syndic.cs_id)
            .join(CombinedStructure, Syndic.cs_id == CombinedStructure.id)
            .filter(Syndic.name == filter["values"][0])
            .label("syndicName")
        )

    @staticmethod
    def build_owner_name_query(filter):
        """
        Lot: Build query manually when searching by owner_name
        """
        return (
            Lot.query.with_entities(Lot.id)
            .join(LotOwner)
            .join(Person)
            .filter(
                and_(
                    LotOwner.c.owner_id == Person.id,
                    LotOwner.c.lot_id == Lot.id,
                    or_(
                        Person.first_name.ilike(filter["values"][0]),
                        Person.last_name.ilike(filter["values"][0]),
                        Person.company_name.ilike(filter["values"][0]),
                    ),
                )
            )
            .label("owners")
        )

    @staticmethod
    def build_lot_mission_id_query(filter):
        """
        Lot: Build query manually when searching by mission_id
        """
        return (
            Lot.query.with_entities(Lot.id)
            .join(Copro, Copro.id == Lot.copro_id)
            .filter(Copro.mission_id == filter["values"][0])
            .label("lotMissionId")
        )

    @staticmethod
    def build_building_mission_id_query(filter):
        """
        Building: Build query manually when searching by mission_id
        """
        return (
            Building.query.with_entities(Building.id)
            .join(Copro, Copro.id == Building.copro_id)
            .filter(Copro.mission_id == filter["values"][0])
            .label("buildingMissionId")
        )
