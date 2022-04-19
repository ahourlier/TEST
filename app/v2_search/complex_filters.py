from sqlalchemy.sql.elements import and_, or_

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
        for filter in search_obj["filters"]:
            # From combined_structure
            if entity == "combined_structure":
                if filter["field"] == "syndic_name":
                    complex_filter[
                        "syndic_name"
                    ] = ComplexFilters.build_syndic_name_query(filter)
                    # Removed because recursiv search couldn't
                    # find this column since it came from another table
                    search_obj["filters"].remove(filter)
            # From lot
            if entity == "lot":
                if filter["field"] == "owner_name":
                    complex_filter[
                        "owner_name"
                    ] = ComplexFilters.build_owner_name_query(filter)
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
                        Person.first_name == filter["values"][0],
                        Person.last_name == filter["values"][0],
                        Person.company_name == filter["values"][0]
                    ),
                )
            )
            .label("owners")
        )
