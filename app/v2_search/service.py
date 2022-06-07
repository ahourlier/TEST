from datetime import datetime
from flask import g
import json
from app.auth.users.model import UserRole
from app.building.model import Building
from app.mission.teams.service import TeamService
from app.v2_search.utils import (
    add_autocomplete_values,
    add_enums_values,
    add_is_default_fields,
    add_label_fields,
    add_many_to_x_fields,
    add_mission_managers,
    add_one_to_one_fields,
    change_column_type,
    filter_by_mission_permission,
    get_structure_from_entity,
)

from .config_structure import (
    ENTITY_TO_MODEL_MAPPING,
)
from .config_sql_relations import (
    ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING,
)

from .complex_filters import ComplexFilters
from app.common.search import SearchService

from app.combined_structure.model import CombinedStructure
from app.lot.model import Lot


class StructureService:
    def build_structure(entity, structure):
        """
        Build whole structure
        """
        structure = get_structure_from_entity(entity, structure)
        structure = add_one_to_one_fields(entity, structure)
        structure = add_many_to_x_fields(entity, structure)
        structure = add_label_fields(entity, structure)
        structure = add_is_default_fields(entity, structure)
        structure = add_enums_values(entity, structure)
        structure = add_autocomplete_values(entity, structure)
        structure = change_column_type(structure)
        return structure


class SearchV2Service:
    def get_one_to_one_references_from_entity(entity):
        """
        Get references from entity
        """
        if entity not in ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING:
            print(f"Entity {entity} has no relation mapper references")
            return None

        return ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING[entity]

    def search_entity(entity, one_to_one_mapper, parameters, operator):
        """
        Build search query from parameters and mapper,
        Perform a recursiv search to manage foreign key columns
        """
        search_obj = SearchV2Service.build_filters_obj(
            one_to_one_mapper, parameters, operator
        )

        # Manage manually complex_filters, ie. Many to One, Many to Many...
        # Filters will be apply as subquery of recursiv search
        complex_filter = ComplexFilters.build_complex_filters(entity, search_obj)

        # Wrapper for apply subquery on search_into_model
        return SearchV2Service.build_querys(entity, search_obj, complex_filter)

    def build_filters_obj(one_to_one_mapper, parameters, operator):
        """
        Build the filters object used by search_into_model recursive query builder
        """
        search = {}
        search["filters"] = []

        for param_column_name, value in parameters.items():
            obj = {}
            obj["values"] = []
            if one_to_one_mapper:
                for column_name, references in one_to_one_mapper.items():
                    # If current column is mapped to a complex field
                    if column_name == param_column_name:
                        obj["field"] = references
            # No mapping found, column is a simple field
            if not "field" in obj:
                obj["field"] = param_column_name

            # Skip term param
            if param_column_name == "term":
                continue

            # Parse the current value to know if it's a list or simple value
            # Manage date differently to allow 'in' and 'range' search
            try:
                value = json.loads(value)
            except ValueError:
                # Here only simple string value
                try:
                    datetime.strptime(value, "%Y-%m-%d")
                    obj["values"].append(value)
                    obj["op"] = "eq"
                    search["filters"].append(obj)
                    continue
                except Exception as e:
                    pass

                # It is a string, not a date, search with IN operator
                obj["values"].append(value)
                obj["op"] = operator
                search["filters"].append(obj)
                continue

            # Here value can be a list or an int
            if isinstance(value, int):
                obj["values"].append(value)
                obj["op"] = "eq"
                search["filters"].append(obj)
                continue

            # Here value is a list
            # Search for range of date
            if len(value) == 2:
                try:
                    datetime.strptime(value[0], "%Y-%m-%d")
                    datetime.strptime(value[1], "%Y-%m-%d")
                    obj["values"] = value
                    obj["op"] = "range"
                    search["filters"].append(obj)
                    continue
                except:
                    pass

            # No range or int found, it's a list of strings, search exact value
            obj["values"] = value
            obj["op"] = "eq"
            search["filters"].append(obj)
        return search

    def build_querys(entity, search_obj, complex_filter):
        """
        Search recursively into model and apply subquery when needed
        """
        # Search recursively from main model
        q = SearchService.search_into_model(ENTITY_TO_MODEL_MAPPING[entity], search_obj)
        # Pass a subquery to perform more filters
        if "syndic_name" in complex_filter:
            q = q.filter(CombinedStructure.id.in_([complex_filter["syndic_name"]]))
        if "owner_name" in complex_filter:
            q = q.filter(Lot.id.in_([complex_filter["owner_name"]]))
        if "mission_id" in complex_filter:
            if entity == "lot":
                q = q.filter(Lot.id.in_([complex_filter["mission_id"]]))
            if entity == "building":
                q = q.filter(Building.id.in_([complex_filter["mission_id"]]))

        # Filter final result by mission permission
        user = g.user
        model = ENTITY_TO_MODEL_MAPPING[entity]
        if user is not None and user.role != UserRole.ADMIN:
            q = filter_by_mission_permission(q, model, user)

        items = q.all()
        # Add manager project on mission
        if entity == "mission":
            items = add_mission_managers(items)
            
        return items
