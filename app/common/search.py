from psycopg2.extensions import JSON
from sqlalchemy.sql.elements import or_, and_

from app.common.exceptions import (
    InvalidSearchFieldException,
    InvalidSearchOperatorException,
)
from app.project import Requester

SEARCH_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="missionType", type=str),
]


def sort_query(query, field=None, direction="asc"):
    if field is not None:
        model = next(query._mapper_entities).type
        if hasattr(model, field):
            col = getattr(model, field)
            query = query.order_by(col.asc() if direction == "asc" else col.desc())
            if field == "updated_at":
                col_2 = getattr(model, "created_at")
                query = query.order_by(
                    col_2.asc() if direction == "asc" else col_2.desc()
                )
            return query
    return query


class SearchService:
    @staticmethod
    def search_into_model(model, search: JSON, search_fields=[]):
        """Main search method. Manage steps in order to apply generic successives filters"""
        q = model.query
        # filter by term
        if "term" in search:
            q = SearchService.filter_by_input_text(q, search_fields, search["term"],)
            del search["term"]
        # apply filters

        q = SearchService.search_on_filters(search["filters"], q)
        return q

    @staticmethod
    def filter_by_input_text(q, search_fields, term):
        """Apply search on input texts. Here filters are applied with an "OR" operator."""
        model = next(q._mapper_entities).type
        term_filters = []
        terms = term.split(" ")
        for t in terms:
            for field in search_fields:
                query_filter = SearchService.build_query(model, field, "in", [t])
                if query_filter is not None:
                    term_filters.append(query_filter)
        q = q.filter(or_(*term_filters))
        return q

    @staticmethod
    def search_on_filters(filters, q):
        """Apply filter, with an "AND" operator."""
        model = next(q._mapper_entities).type
        for filter in filters:
            query_filter = SearchService.build_query(
                model, filter["field"], filter["op"], filter["values"]
            )
            if query_filter is not None:
                q = q.filter(query_filter)
        return q

    @staticmethod
    def build_query(model, search, op, values):
        """Build a query recursively to dive into the "search" field hierarchy """
        splitted_search = search.split(".")
        property = getattr(model, splitted_search[0], None)
        if not property:
            raise InvalidSearchFieldException()
        # If there is no values to look for, no need for building a query
        if not values:
            return None
        has_value = False
        for val in values:
            if val is not None:
                has_value = True
        if not has_value:
            return None
        # If search has only one layer. ex : "id". Query on parent Table, which is the initial "model" params
        if len(splitted_search) == 1:
            return SearchService.apply_filter(property, op, values)
        # If search has two layers. ex : "mission.id". Query on child Table after field determination
        elif len(splitted_search) == 2:
            sub_model = property.mapper.class_
            field = getattr(sub_model, splitted_search[1], None)
            # If property is a collection of object, the SQLAlchemy function to use is "any".
            # Else, it's "has"
            if property.impl.collection:
                return property.any(SearchService.apply_filter(field, op, values))
            else:
                return property.has(SearchService.apply_filter(field, op, values))
        # If search has more than two layers. Must recur while building the nested query. ex : mission.antenna.id
        # Continues until reaching the "search bottom" (i.e. when only two layers remains)
        else:
            sub_model = property.mapper.class_
            del splitted_search[0]
            search = ".".join(splitted_search)
            # If property is a collection of object, the SQLAlchemy function to use is "any".
            # Else, it's "has"
            if property.impl.collection:
                return property.any(
                    SearchService.build_query(sub_model, search, op, values)
                )
            else:
                return property.has(
                    SearchService.build_query(sub_model, search, op, values)
                )

    @staticmethod
    def apply_filter(field, op, values):
        """Apply a filter on a specific field, looking for a correspondance within the values list """

        # As targetted values, we may receive a list of IDs OR plain dicts from the front-app.
        # If plain dicts, we need here to flatten values by extracting their ids
        for i, value in enumerate(values):
            if isinstance(value, dict):
                values[i] = value.get(field.property.key)

        # Apply filters, depending on op (operator) type.
        if not field:
            raise InvalidSearchFieldException()
        if op == "eq":
            return or_(*[field == value for value in values if value is not None])
        elif op == "gte":
            return or_(*[field >= value for value in values if value is not None])
        elif op == "gt":
            return or_(*[field > value for value in values if value is not None])
        elif op == "lte":
            return or_(*[field <= value for value in values if value is not None])
        elif op == "lt":
            return or_(*[field < value for value in values if value is not None])
        elif op == "in":
            return or_(
                *[field.ilike(f"%{value}%") for value in values if value is not None]
            )
        elif op == "range":
            if len(values) != 2:
                raise InvalidSearchFieldException()
            values.sort()
            return and_(field >= values[0], field <= values[1])
        elif op == "range-exc":
            if len(values) != 2:
                raise InvalidSearchFieldException()
            values.sort()
            return and_(field > values[0], field < values[1])
        else:
            raise InvalidSearchOperatorException()
