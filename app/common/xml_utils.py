import logging
import xml.etree.cElementTree as ET
from enum import Enum
from random import random, uniform, randrange
from typing import List

from flask_restx import abort

from app import db
from app.common.config_error_messages import (
    KEY_XML_CONFLICTING_ROOTS_EXCEPTION,
    KEY_XML_MISSING_CONFIGURATION_INFOS_EXCEPTION,
    KEY_XML_MISSING_ROOT_EXCEPTION,
    KEY_XML_MISSING_CONFIGURATION_FIELDS,
    KEY_XML_INVALID_ITERATION_PARENT,
)
from app.common.exceptions import XMLGenerationException
from app.common.services_utils import ServicesUtils
from app.common.templating_utils import TemplatingUtils
from app.referential.enums import PerrenoudEnum


class StructureTypes(Enum):
    CONTAINER = "container"
    ITERATION = "iteration"
    ITERATION_CHILD = "iteration_child"


class IdentityRoles(Enum):
    PRIMARY = "primary"
    FOREIGN = "foreign"


class PerrenoudTypes(Enum):
    EXT_WALL = "exterior_wall"
    EXT_WALL_ON_LNC = "exterior_wall_on_LNC"
    CEILING = "ceiling"
    FLOOR = "floor"
    HEATING = "heating"


PERRENOUD_RESPONSE_CODES = {
    "exterior_wall": "TR014_001",
    "exterior_wall_on_LNC": "TR014_002",
    "ceiling": "TR014_003",
    "floor": "TR014_004",
    "heating": "TR003_001",
}


class XMLBuilder:
    """
    This class util has to purpose to build a complete XML, based on XML_Configuration file.
    The XML configuration file is built as a list of dict. Each dict represents an "item of the XML"

    *** Some useful terms I used here ***
    - I call "item" a member of the configuration dict. Each "item" fits a line
    provided from the "Mapping OSLO - Perrenoud" spreadsheet.
    - An "element", in the present module, is a tag instanciated into the xml.
    Each item, depending on his configurations elements, can be instanciated to one
    OR SEVERAL "elements". Don't make the confusion, or you are doomed to understand
    this mess :-)

     *** XMLUtils members ***

    - self.xml_configuration : (list of dicts). Main config variable. List of "items" that will be instanciated,
    depending on their configuration fields. (See "Build XML Configuration" section below)
    - self.base_db_entity : base database entity in which the xml data will be fetched. (For Perrenoud,
    it's always a Scenario Entity)
    - self.xml_generation_map : A map, auto-completed during the generation process, such as :
    {"<id_element>" : {"instances" : {ElementObject : some_db_entity, etc.} }.
    Used to set parent/children relationships between elements.
    - self.foreign_keys_map : A map, auto-completed during the generation process, such as :
    {"db_tablename" : {"db_entity_id" : "primary_key_id"}}. Used to link primary/foreign key.
    - self.last_id_incremented : (int) auto_increment number for primary key auto generated into the xml.
    (Dirty tricks here : I set it to "1" in order to the first ID be always "2". Why ? Because the id "1" is
    used as the "Generation" unique ID. (See Perrenoud XML Model.)
    - self.root : Element Object used as the root of the XML.


    *** Build XML Configuration ***

    XML Configuration Variable, injected into XMLUtils is a list of dicts, each one representing an item that will be instanciated in the XML.
    Here are the fields possibly used to configure these elements :

    - "id" : <The tag id> (used to identify the element)
    - "is_root" : True/False (If the element is root fo the built XML. The "is_root" item must
    be the first of the list. That's not perfect. I should have separated this item from the others.
    You can still refactor it)
    - "tag" : <the tag name>
    - "parent" : <id of the parent> | "root" (if parent is root)
    - "structure_type" : None | "iteration" (for repeated tags over a list of entities)
    - "identity_role" : None | "primary" (elements that contain a "primary identifiant key". An int generated during the XML process that identify a given entity)
    | "foreign" (elements that contain a "foreign identifiant key").
    - "has_value" : None | True (if tag display a value) | False, (Interpreted as False if None)
    - "fields" : name of the parameters fields fetched from the database base entity
    - "constant" : can be set for xml tag that always have the same value
    - "rule" : name of the method used to fetch value (or to fetch foreign key)
    - "enum_index" : if necessary, enum_index used to convert "string value" (label) to actual "perrenoud value"
    """

    def __init__(self, xml_configuration, base_db_entity):
        self.xml_configuration = ServicesUtils.deep_copy_list_of_dicts(
            xml_configuration
        )
        self.base_db_entity = base_db_entity
        self.xml_generation_map = {}
        self.foreign_keys_map = {}
        self.last_id_incremented = 1
        self.root = self.instanciate_root()
        self.missing_elements = []

    def main_build_xml(self):
        # XML generation starts and ends here
        for item in self.xml_configuration:
            if "structure_type" not in item or not item.get("structure_type"):
                item["structure_type"] = []
            if not isinstance(item.get("structure_type"), list):
                item["structure_type"] = [item.get("structure_type")]
            parent_elements = self.fetch_parent_element(item)
            if parent_elements is None:
                continue
            self.build_new_item(item, parent_elements)

        return (
            ET.tostring(self.root, encoding="unicode", method="xml"),
            self.missing_elements,
        )

    def build_new_item(self, item, parent_elements):
        """
        New item of the xml is built.
        This central step can lead to the instanciation of one OR several elements
        """

        valid_item, error_message = self.check_item_validity(item)
        if valid_item is False:
            raise XMLGenerationException(error_message, item.get("tag"))

        # Iterated elements building
        if StructureTypes.ITERATION.value in item.get("structure_type"):
            self.build_iteration(item, parent_elements)
            return
        # Unique element building
        self.instanciate_elements(item, parent_elements)

    def instanciate_elements(self, item, parent_elements):
        """Instanciate an element, set his content and update the
        generation map"""
        for element, entity in parent_elements.items():
            self.instanciate_element(item, element, entity)

    def instanciate_element(self, item, element, entity):
        new_element = ET.SubElement(element, item.get("tag"))
        self.set_element_value(new_element, entity, item)
        self.update_generation_map(new_element, item, entity)

    def update_generation_map(self, new_element, item, entity):
        """Each time an element is created, monitoring collection xml_generation_map must be updated"""
        ServicesUtils.set_nested_dict(
            self.xml_generation_map,
            [item.get("id"), "instances"],
            {new_element: entity},
            append=True,
        )

    def build_iteration(self, item, parent_elements):
        """Build an iterated item (this item will be instanciated
        for each entity of the list pointed by the fields of the item)"""
        item.get("structure_type").remove(StructureTypes.ITERATION.value)
        for parent_element, parent_entity in parent_elements.items():
            entities_to_iterate_on = self.fetch_entities_to_iterate(item, parent_entity)
            if not entities_to_iterate_on:
                logging.info(
                    f"Item ID {item.get('id')} not instanciated. No corresponding db entities were found to iterate"
                )
                if self.is_item_mandatory(item):
                    self.missing_elements.append(
                        {
                            "error_type": "EMPTY MANDATORY COLLECTION",
                            "xml_id": item.get("id"),
                            "tag_name": item.get("tag"),
                        }
                    )
                return
            for entity in entities_to_iterate_on:
                self.instanciate_element(item, parent_element, entity)

    def fetch_iteration_elements(self, iteration_element_id):
        parent_iterations_map = self.fetch_parent_iterations(iteration_element_id)
        if not parent_iterations_map:
            return
        return parent_iterations_map.get("instances")

    def set_element_value(self, element, entity, item):
        """Creates and returns an 'instance' of an iteration child. Each iteration child has as many elements
        instanciated as the iteration size"""
        if element is None:
            logging.error(
                f"Item ID {item.get('id')} not instanciated. No element to set"
            )

        if item.get("identity_role") == IdentityRoles.PRIMARY.value:
            self.set_primary_key(element, item, entity)
        if item.get("identity_role") == IdentityRoles.FOREIGN.value:
            self.set_foreign_key(element, item, entity)
        if item.get("has_value") is True:
            self.set_raw_value(element, entity, item)

        is_element_textual = (
            item.get("identity_role")
            or item.get("identity_role")
            or item.get("has_value")
        )
        if is_element_textual and not self.is_value_compliant(item, element, entity):
            self.missing_elements.append(
                {
                    "error_type": "MISSING MANDATORY VALUE",
                    "xml_id": item.get("id"),
                    "tag_name": item.get("tag"),
                    "entity_name": entity.__tablename__,
                    "entity_id": entity.id,
                }
            )
        return element

    def set_primary_key(self, element, item, entity):
        """Primary key elements are tags containing a specific 'ID', auto-incremented, which allows
        to identify the object within other tags.
        Example :   <Mur_collection>
                    <Mur><primary_key_element>1</primary_key_element></Mur>
                    <Mur><primary_key_element>2</primary_key_element></Mur>
                    </Mur_collection>
                    ...
                    <Mur sélectionné>
                        <foreign_key_element> 1 </foreign_key_element>
                    </Mur sélectionné>
        """
        if entity is None:
            logging.error(
                f"Item ID {item.get('id')} not instanciated. No corresponding entity"
            )
        entity_model = entity.__table__.name
        entity_id = entity.id
        new_primary_key = self.last_id_incremented + 1
        self.last_id_incremented = new_primary_key
        self.set_raw_value(element, entity, item, value=new_primary_key)
        ServicesUtils.set_nested_dict(
            self.foreign_keys_map, [entity_model, entity_id], new_primary_key,
        )

    def set_foreign_key(self, new_element, item, entity):
        """Foreign key elements are tags containing an 'ID' pointing to others elements. Link is done
        through this ID (see build_foreign_key_element method)"""

        foreign_key_id = self.fetch_foreign_key(item, entity)
        self.set_raw_value(new_element, entity, item, value=foreign_key_id)
        return new_element

    def fetch_parent_element(self, item):
        """Given a provided item, fetch all instances (elements) corresponding to the item's parent"""
        try:
            return (
                self.xml_generation_map.get(item.get("parent")).get("instances")
                if item.get("parent") != "root"
                else {self.root: self.base_db_entity}
            )
        except:
            logging.info(
                f"No parent found for item {item.get('tag')}. This item will not be instanciated"
            )
            return None  # No parent found. Instanciation must be canceled

    def fetch_entities_to_iterate(self, item, parent_entity):
        """Given a parent database entity, returns a list of sub_entities corresponding to the
        wanted field and rule of the item"""
        if not item.get("fields"):
            raise XMLGenerationException(
                KEY_XML_MISSING_CONFIGURATION_FIELDS, item.get("tag")
            )
        if isinstance(parent_entity, list):
            return parent_entity
        return self.fetch_data(parent_entity, item.get("fields"), item.get("rule"),)

    def fetch_parent_iterations(self, parent_id):
        """Given a parent_id, fetch all elements instanciated from it."""
        parent_iteration_map = self.xml_generation_map.get(parent_id)
        if "instances" not in parent_iteration_map or not parent_iteration_map.get(
            "instances"
        ):
            # No parent has been instanciated. Children cannot be instanciated either
            return None
        return parent_iteration_map

    def check_item_validity(self, item):
        """Return a Boolean and a state message that indicates the validity of the item."""
        if (
            not item.get("tag")
            or not item.get("id")
            or (not item.get("parent") and not item.get("is_root"))
        ):
            return False, KEY_XML_MISSING_CONFIGURATION_INFOS_EXCEPTION
        if item.get("is_root") is True:
            return False, KEY_XML_CONFLICTING_ROOTS_EXCEPTION
        return True, "success"

    def is_value_compliant(self, item, element, entity):
        """Return True if an element is mandatory and have a non-null value or is not mandatory at all,
        else False"""
        if not self.is_item_mandatory(item, current_entity=entity):
            return True
        if not item.get("validation") or (
            item.get("validation").get("mandatory")
            and item.get("validation").get("mandatory") is True
        ):
            return element.text is not None
        return True

    def is_item_mandatory(self, item, current_entity=None):
        """Given a set of conditions, return True if elements for this item
        will be mandatory, else False"""
        if not item.get("validation"):
            return True
        conditions = item.get("validation").get("conditions")
        if not conditions or self.check_conditions(conditions, current_entity):
            return item.get("validation").get("mandatory")
        else:
            return not item.get("validation").get("mandatory")

    def check_conditions(self, conditions, current_entity):
        """Check recursively all mandatory conditions by And or Or keyword."""
        if isinstance(conditions, dict):
            return self.is_condition_fulfilled(conditions, current_entity)
        if conditions[0] != "and" and conditions[0] != "or":
            return False
        if conditions[0] == "and":
            conditions.pop(0)
            for sub_condition in conditions:
                if not self.check_conditions(sub_condition, current_entity):
                    return False
            return True
        if conditions[0] == "or":
            conditions.pop(0)
            for sub_condition in conditions:
                if self.check_conditions(sub_condition, current_entity):
                    return True
            return False
        return False

    def is_condition_fulfilled(self, condition, current_entity):
        """Return True if one specific condition is fulfilled, esle False"""
        target_item = self.xml_generation_map.get(condition.get("id"))
        target_element = self.find_target_element(target_item, current_entity)
        if target_element is None:
            return False
        if not self.check_value_by_operator(
            target_element.text, condition.get("value"), condition.get("operator")
        ):
            return False
        return True

    def find_target_element(self, target_item, current_entity):
        """Within the previously generated XML, find and return the element/tag
        targetted by the given condition"""
        if not target_item.get("instances") or len(target_item.get("instances")) < 1:
            return None
        if len(list(target_item.get("instances"))) == 1:
            return list(target_item.get("instances").keys())[0]
        else:
            for element, entity in target_item.get("instances").items():
                if entity == current_entity:
                    return element
        return None

    def check_value_by_operator(self, value, target_value, operator):
        """Return True if value is compliant with target-value, given the operator,
        else False"""
        value = float(value) if value else None
        if not value:
            return False
        target_value = float(target_value)
        if operator == "<":
            return value < target_value
        elif operator == "<=":
            return value <= target_value
        elif operator == ">":
            return value > target_value
        elif operator == ">=":
            return value >= target_value
        elif operator == "==":
            return value == target_value
        elif operator == "!=":
            return value != target_value
        elif operator == "in":
            if not isinstance(target_value, list):
                target_value = [target_value]
                return value in target_value
        return False

    def fetch_foreign_key(self, item, entity):
        """Given an item and a database_entity, fetch the 'key' corresponding to the wanted 'foreign key'"""
        mapping_rule_name = (
            item.get("mapping_foreign_entity_rule")
            if item.get("mapping_foreign_entity_rule")
            else "basic_fetch_foreign_key"
        )
        fetch_foreign_key_rule = getattr(
            PerrenoudFetchRulesCollection, mapping_rule_name
        )
        return fetch_foreign_key_rule(
            entity,
            item.get("fields"),
            item.get("foreign_linked_entity"),
            self.foreign_keys_map,
        )

    def set_raw_value(self, element, entity, item, value=None):
        """Set a value within a XML tag. Example : <My_Element> Fetched_Value </My_Element>"""
        if value:
            element.text = str(value)
            return element
        if item.get("constant"):
            element.text = str(item.get("constant"))
            return element
        if not item.get("fields"):
            raise XMLGenerationException(
                KEY_XML_MISSING_CONFIGURATION_FIELDS, item.get("tag")
            )
        if entity is None:
            logging.error(
                f"Item ID {item.get('id')} not instanciated. No corresponding entity"
            )
        value = self.fetch_data(
            entity,
            item.get("fields"),
            item.get("rule"),
            enum_index=item.get("enum_index"),
        )
        element.text = value
        return element

    def fetch_data(self, entity, fields, rule_name, enum_index=None):
        """For a given XML node, fields and corresponding rules, fetch the value in database.
        Optionaly, can give an enum_index to convert the raw value into a Perrenoud enum integer value"""
        if not rule_name:
            rule_name = "get_basic_value"
        apply_rule = getattr(PerrenoudFetchRulesCollection, rule_name)
        try:
            data = apply_rule(entity, fields)
        except:
            logging.error(f"ERROR while fetching field {fields} from entity {entity}")
            return None

        if enum_index:
            try:
                return PerrenoudFetchRulesCollection.fetch_perrenoud_enum_value(
                    data, enum_index
                )
            except Exception as e:
                logging.error(
                    f"ERROR while fetching perrenoud value. Converted value : {data}. Perrenoud Index : {enum_index}"
                )
                return None

        return data

    def instanciate_root(self):
        """Instanciante the first item of the configuration list, which must be a roo"""
        root_item = self.xml_configuration.pop(0)
        if root_item.get("is_root") is False:
            raise XMLGenerationException(
                KEY_XML_MISSING_ROOT_EXCEPTION, root_item.get("tag")
            )
        root = ET.Element(root_item.get("tag"))
        return root


class PerrenoudFetchRulesCollection:
    """Class acting as a collection of custom business rules ready to be used within the XML generation.
    Theses rules are designed to fit the needs of the Perrenoud webservice"""

    @staticmethod
    def fetch_perrenoud_enum_value(label, enum_index):
        """Returns an integer value (stringified) correspond to the provided label and Perrenoud Enum"""
        if label and not isinstance(label, (float, str, int)):
            logging.error(
                f"ERROR : {label} value does not match any value within perrenoud enum number {enum_index}"
            )
            return None
        enum = (
            db.session.query(PerrenoudEnum)
            .filter(PerrenoudEnum.index == enum_index)
            .filter(PerrenoudEnum.label == label)
            .first()
        )
        if not enum:
            return None
        return str(enum.value)

    @staticmethod
    def get_basic_value(entity, fields):
        """Basic, default route. Fetch in database the value corresponding to the provided parent entity and fields path.
        Example : entity = scenario, fields = "", "annual_energy_consumption"""
        if not isinstance(fields, list):
            fields = [fields]
        value = TemplatingUtils.fetch_standard_field_value(fields[0], entity).get(
            "value"
        )
        if value and isinstance(value, bool):
            bool_to_int = {True: "1", False: "0"}
            return bool_to_int.get(value)
        if value and not isinstance(value, list):
            return str(value)
        return value

    @staticmethod
    def basic_fetch_foreign_key(entity, field, foreign_linked_entity, foreign_keys_map):
        """Basic, default foreign key method."""
        if isinstance(foreign_linked_entity, list):
            foreign_linked_entity = foreign_linked_entity[0]
        if isinstance(field, list):
            field = field[0]
        foreign_db_entity_id = getattr(entity, field)
        linked_entities_map = foreign_keys_map.get(foreign_linked_entity)
        if not linked_entities_map:
            logging.error(
                f"Impossible to set foreign key {field} into entity {entity}."
            )
            return None
        return linked_entities_map.get(foreign_db_entity_id)

    @staticmethod
    def get_department_number(entity, field):
        """Given an address code, return a 'department' number"""
        code = entity.accommodation.project.address_code
        if code:
            code = code[:-3]
        return code

    @staticmethod
    def get_living_area(entity, field):
        """Fetch living area, calculated or given"""
        if entity.accommodation.living_area:
            return str(entity.accommodation.living_area)
        else:
            return str(entity.total_living_area)

    @staticmethod
    def get_initial_state_status(entity, field):
        """Return 0 if is initial state, 1 for scenario"""
        return "0" if entity.is_initial_state else "1"

    @staticmethod
    def get_insulation_return(entity, field):
        """Return "1" wall is insulated. Else "0" """
        return "1" if entity.insulated_wall is True else "0"

    @staticmethod
    def has_seal(entity, field):
        """Business custom rule for field 84,'Lst011_Avec_Joint'"""
        field_91_value = PerrenoudFetchRulesCollection.fetch_perrenoud_enum_value(
            entity.glass_type, 24
        )
        if field_91_value == "0" or field_91_value == "1":
            return "0"
        else:
            return "1"

    @staticmethod
    def get_regulation_by_room(entity, field):
        """Business rule for field number 258 :
        ""Lst011_Regul_Piece"" field"""
        emettor_type_value = PerrenoudFetchRulesCollection.fetch_perrenoud_enum_value(
            entity.emettor_type, 43
        )
        if emettor_type_value in [
            202,
            208,
            302,
            308,
            402,
            408,
            502,
            508,
            602,
            608,
            704,
            710,
        ]:
            return "1"
        return "0"

    @staticmethod
    def get_construction_year(scenario, field):
        """From Perrenoud enum index 002 (hardcoded below), return an corresponding value"""
        construction_year = scenario.accommodation.construction_year
        if scenario.accommodation.project.requester.type == "PO":
            construction_year = scenario.accommodation.construction_year
        else:
            construction_year = (
                scenario.accommodation.project.common_areas.construction_year
            )

        if construction_year is None:
            return None
        intervals_list = {
            (0, 1974): "1",
            (1975, 1977): "2",
            (1978, 1982): "3",
            (1983, 1988): "4",
            (1989, 2000): "5",
            (2001, 2005): "6",
            (2006, 3000): "7",
        }
        for interval, value in intervals_list.items():
            if interval[0] <= construction_year <= interval[1]:
                return value

        return None

    @staticmethod
    def get_generator_energy(heating, field):
        """Given a heating, return the energy type value (as
        described into the enum 0038 Perrenoud, hardcoded below)"""
        energy_correspondance = {
            "Fioul": "0",
            "Gaz": "1",
            "Bois": "2",
            "Charbon": "3",
            "Electrique thermodynamique": "4",
            "Electrique effet joule": "5",
        }
        if heating.energy_used:
            return energy_correspondance.get(heating.energy_used)
        return None

    @staticmethod
    def get_power(heating, field):
        """Return value power for "Generation" structure into Perrenoud XML"""
        return str(heating.power) if heating.is_power_known is True else "-1"

    @staticmethod
    def get_network_type(heating, field):
        """Perrenoud business rule. Fetch network type"""
        emissions_type = int(
            PerrenoudFetchRulesCollection.fetch_perrenoud_enum_value(
                heating.emissions_type, 41
            )
        )
        generator_type = int(
            PerrenoudFetchRulesCollection.fetch_perrenoud_enum_value(
                heating.generator_type, 39
            )
        )
        if emissions_type == 1:

            if generator_type in [107, 108, 207, 208, 211, 503, 504, 505]:
                return "2"
            elif generator_type == 502:
                return "3"
            else:
                return "1"
        elif emissions_type == 2:
            if generator_type in [107, 108, 207, 208, 211, 503, 504, 505]:
                return "5"
            elif generator_type == 502:
                return "6"
            else:
                return "4"
        else:
            return None

    @staticmethod
    def has_gaz_heating(scenario, field):
        """Return "1" if at least one gaz hearting is present"""
        for heating in scenario.heatings:
            if heating.energy_used == "Gaz":
                return "1"
        return "0"

    @staticmethod
    def get_building_type(scenario, field):
        """Return 2 if apartment, else 1"""
        return (
            "2" if scenario.accommodation.accommodation_type == "Appartement" else "1"
        )

    @staticmethod
    def get_known_caracteristics(heating, field):
        # Business rule for ID-238, Lst011_Caracteristiques_Connues"

        if heating.scenario.is_initial_state is True:
            return None
        generator_type = int(
            PerrenoudFetchRulesCollection.fetch_perrenoud_enum_value(
                heating.generator_type, 39
            )
        )
        if 301 <= generator_type <= 399 or 501 <= generator_type <= 599:
            return "1" if heating.known_caracteristics is True else "0"
        return "0"


PERRENOUD_RESPONSE_CODES = {
    "exterior_wall": "TR014_001",
    "exterior_wall_on_LNC": "TR014_002",
    "floor": "TR014_003",
    "ceiling": "TR014_004",
    "heating": "TR003_001",
    "heating_energy_final": "TR006_001",
    "hot_water_energy_final": "TR006_002",
    "cooling_energy_final": "TR006_003",
}


class PerrenoudParser:
    """Class dedicated to Perrenoud response parsing"""

    @staticmethod
    def parse_xml(xml):
        """Parse XML and returns Perrenoud results changes for a scenario"""

        root = ET.fromstring(xml)

        (
            heat_energy_1_final,
            heat_energy_2_final,
        ) = PerrenoudParser.fetch_energy_consumption(
            root,
            fields=[
                "consommation_energie_finale",
                "tr006_type_usage_id",
                "tr004_type_energie_id",
            ],
            conditions={
                "tr006_type_usage_id": PERRENOUD_RESPONSE_CODES.get(
                    "heating_energy_final"
                )
            },
            summed_field="consommation_energie_finale",
        )
        (
            ECS_energy_1_final,
            ECS_energy_2_final,
        ) = PerrenoudParser.fetch_energy_consumption(
            root,
            fields=[
                "consommation_energie_finale",
                "tr006_type_usage_id",
                "tr004_type_energie_id",
            ],
            conditions={
                "tr006_type_usage_id": PERRENOUD_RESPONSE_CODES.get(
                    "hot_water_energy_final"
                )
            },
            summed_field="consommation_energie_finale",
        )
        (
            cooling_energy_1_final,
            cooling_energy_2_final,
        ) = PerrenoudParser.fetch_energy_consumption(
            root,
            fields=[
                "consommation_energie_finale",
                "tr006_type_usage_id",
                "tr004_type_energie_id",
            ],
            conditions={
                "tr006_type_usage_id": PERRENOUD_RESPONSE_CODES.get(
                    "cooling_energy_final"
                )
            },
            summed_field="consommation_energie_finale",
        )
        (
            heat_energy_1_primary,
            heat_energy_2_primary,
        ) = PerrenoudParser.fetch_energy_consumption(
            root,
            fields=[
                "consommation_energie_primaire",
                "tr006_type_usage_id",
                "tr004_type_energie_id",
            ],
            conditions={
                "tr006_type_usage_id": PERRENOUD_RESPONSE_CODES.get(
                    "heating_energy_final"
                )
            },
            summed_field="consommation_energie_primaire",
        )
        (
            ECS_energy_1_primary,
            ECS_energy_2_primary,
        ) = PerrenoudParser.fetch_energy_consumption(
            root,
            fields=[
                "consommation_energie_primary",
                "tr006_type_usage_id",
                "tr004_type_energie_id",
            ],
            conditions={
                "tr006_type_usage_id": PERRENOUD_RESPONSE_CODES.get(
                    "hot_water_energy_final"
                )
            },
            summed_field="consommation_energie_primary",
        )
        (
            cooling_energy_1_primary,
            cooling_energy_2_primary,
        ) = PerrenoudParser.fetch_energy_consumption(
            root,
            fields=[
                "consommation_energie_primaire",
                "tr006_type_usage_id",
                "tr004_type_energie_id",
            ],
            conditions={
                "tr006_type_usage_id": PERRENOUD_RESPONSE_CODES.get(
                    "cooling_energy_final"
                )
            },
            summed_field="consommation_energie_primaire",
        )

        changes = {
            "annual_energy_consumption": PerrenoudParser.fetch_unique_element(
                [], root, "consommation_energie"
            ),
            "energy_label": PerrenoudParser.fetch_unique_element(
                [], root, "classe_consommation_energie"
            ),
            "annual_GES_emission": PerrenoudParser.fetch_unique_element(
                [], root, "estimation_ges"
            ),
            "GES_label": PerrenoudParser.fetch_unique_element(
                [], root, "classe_estimation_ges"
            ),
            "loss_exterior_wall": PerrenoudParser.fetch_deperditions_repartition(
                root, PERRENOUD_RESPONSE_CODES.get("exterior_wall")
            ),
            "loss_local_wall": PerrenoudParser.fetch_deperditions_repartition(
                root, PERRENOUD_RESPONSE_CODES.get("exterior_wall_on_LNC")
            ),
            "loss_floor": PerrenoudParser.fetch_deperditions_repartition(
                root, PERRENOUD_RESPONSE_CODES.get("floor")
            ),
            "loss_ceiling": PerrenoudParser.fetch_deperditions_repartition(
                root, PERRENOUD_RESPONSE_CODES.get("ceiling")
            ),
            "loss_heat_bridges": PerrenoudParser.fetch_deperdition_bridges(root),
            "loss_airflow": PerrenoudParser.fetch_deperdition_airflow(root),
            "heat_energy_1_final": heat_energy_1_final,
            "heat_energy_1_primary": heat_energy_1_primary,
            "heat_energy_2_final": heat_energy_2_final,
            "ECS_energy_1_final": ECS_energy_1_final,
            "ECS_energy_1_primary": ECS_energy_1_primary,
            "ECS_energy_2_final": ECS_energy_2_final,
            "ECS_energy_2_primary": ECS_energy_2_primary,
            "cooling_energy_1_final": cooling_energy_1_final,
            "cooling_energy_1_primary": cooling_energy_1_primary,
            "cooling_energy_2_final": cooling_energy_2_final,
            "cooling_energy_2_primary": cooling_energy_2_primary,
        }
        return changes

    @staticmethod
    def fetch_deperditions_repartition(root, type_paroi):
        """Business rule.
        Deperdition repartition = sum thermal deperdition / deperdition envelope"""
        thermal_depertition_sum = PerrenoudParser.fetch_summed_elements(
            root,
            path=["le_batiment", "parois_opaques", "item"],
            fields=["deperdition_thermique", "tr014_type_paroi_id"],
            summed_field="deperdition_thermique",
            conditions={"tr014_type_paroi_id": type_paroi},
        )
        deperdition_envelope = PerrenoudParser.fetch_unique_element(
            ["le_batiment"], root, "deperdition_enveloppe"
        )
        if (
            thermal_depertition_sum
            and deperdition_envelope
            and deperdition_envelope != 0
        ):
            return int((thermal_depertition_sum / deperdition_envelope * 100))
        return None

    @staticmethod
    def fetch_deperdition_bridges(root):
        """Business rule.
        Deperdition bridge = ((deperdition_envelope - sum_bridge_deperditions) / sum_bridge_deperditions) * 100"""
        deperdition_envelope = PerrenoudParser.fetch_unique_element(
            ["le_batiment"], root, "deperdition_enveloppe"
        )
        sum_bridge_deperditions = PerrenoudParser.fetch_summed_elements(
            root,
            path=["le_batiment", "parois_opaques", "item"],
            fields=["deperdition_thermique"],
            summed_field="deperdition_thermique",
        )
        return (
            int(
                (
                    (deperdition_envelope - sum_bridge_deperditions)
                    / sum_bridge_deperditions
                )
                * 100
            )
            if sum_bridge_deperditions
            else None
        )

    @staticmethod
    def fetch_deperdition_airflow(root):
        """Business rule.
        Deperdition airflow = (airflow_reuse_loss / deperdition_envelope) * 100"""
        air_flow_reuse_loss = float(
            PerrenoudParser.fetch_unique_element(
                ["le_batiment"], root, "deperdition_renouvellement_air"
            )
        )
        deperdition_envelope = float(
            PerrenoudParser.fetch_unique_element(
                ["le_batiment"], root, "deperdition_enveloppe"
            )
        )
        if air_flow_reuse_loss and deperdition_envelope and deperdition_envelope != 0:
            return int((air_flow_reuse_loss / deperdition_envelope) * 100)
        return None

    @staticmethod
    def fetch_energy_consumption(root, fields, conditions, summed_field):
        """Fetch energy consumptions, sorted by type (energy 1 and energy 2)"""
        elements = PerrenoudParser.find_subelement(
            ["consommations", "item"], root, fields
        )
        elements = PerrenoudParser.filter_list_elements(elements, conditions)
        sorted_elements = PerrenoudParser.sort_by_field(
            elements, "tr004_type_energie_id"
        )
        energy_1_sum = None
        energy_2_sum = None

        if len(sorted_elements.values()) >= 1:
            energy_1_sum = PerrenoudParser.sum_list(
                list(sorted_elements.values())[0], summed_field, cast_type="float"
            )
        if len(sorted_elements.values()) >= 2:
            energy_2_sum = PerrenoudParser.sum_list(
                list(sorted_elements.values())[1], summed_field, cast_type="float"
            )
        return energy_1_sum, energy_2_sum

    @staticmethod
    def sort_by_field(elements: List, sorting_field: str):
        """elements : a list of dicts
        Sort elements regarding to their sorting_field value.
        Returns the result as a dict where different sorting_field values are sorting keys."""
        result = {}
        for element in elements:
            if element.get(sorting_field):
                ServicesUtils.set_nested_dict(
                    result, [element.get(sorting_field)], [element], append=True,
                )
        return result

    @staticmethod
    def fetch_summed_elements(root, path, fields, summed_field, conditions=None):
        """Given a root, a path, and required fields, fetch elements, then sum them
        Alternatively : can filter elements by a given condition before summing"""
        elements_thermal_deperdition = PerrenoudParser.find_subelement(
            path, root, fields
        )
        if conditions:
            elements_thermal_deperdition = PerrenoudParser.filter_list_elements(
                elements_thermal_deperdition, conditions
            )
        return PerrenoudParser.sum_list(elements_thermal_deperdition, summed_field)

    @staticmethod
    def sum_list(elements: List, summed_field: str, cast_type="int"):
        """Returns the sum of the summed_fields extracted from each dict element of the provided elements list"""
        formatted_list = [
            element.get(summed_field)
            for element in elements
            if element.get(summed_field)
        ]
        if cast_type == "int":
            return int(sum(formatted_list))
        elif cast_type == "float":
            return float(sum(formatted_list))
        return sum(formatted_list)

    @staticmethod
    def filter_list_elements(elements_list: List, conditions: dict):
        """fields_list : a list of dict. conditions : a dict where keys are conditioned fields, and values
        required values for theses fields.
        Remove elements from elements_list if they do not match all given conditions"""
        result = []
        for element in elements_list:
            item_validated = True
            for key, value in conditions.items():
                if element[key] != value:
                    item_validated = False
                    break
            if item_validated:
                result.append(element)
        return result

    @staticmethod
    def fetch_unique_element(path, root, field):
        """Find an element and return the given subelement"""
        items = PerrenoudParser.find_subelement(path, root, field)
        return items[0].get(field)

    @staticmethod
    def find_subelement(path: List, node, fields):
        """Fetch all elements matching a given path. Returns a list of formatted dict"""
        if len(path) == 0:
            return [PerrenoudParser.parse_element(node, fields)]
        if len(path) > 1:
            values = []
            for sub_node in node.findall(path[0]):
                sub_path = path.copy()
                sub_path.pop(0)
                sub_values = PerrenoudParser.find_subelement(sub_path, sub_node, fields)
                if sub_values:
                    values = values + sub_values
            return values
        else:
            target_element = node.find(path[0])
            if not target_element:
                return None
            parsed_item = PerrenoudParser.parse_element(target_element, fields)
            if parsed_item is not None:
                return [parsed_item]
            else:
                return None

    @staticmethod
    def parse_element(element_parent, fields):
        """Returns targetted fields within an XML element (as a dict of field_name:value)"""
        if not isinstance(fields, list):
            fields = [fields]
        item = {}
        for field in fields:
            element = element_parent.find(field)
            if element is not None:
                try:
                    item[field] = float(element.text)
                except:
                    item[field] = element.text
        return item if item else None
