import sql_helper
import firestore_helper
from fields_config import building_fields, lot_fields


def process_building(building_id, sql_engine, firestore_client, version):
    # get all lots to get all items required
    lot_ids = sql_helper.get_children_ids(
        sql_engine,
        {"children_table": "lot", "parent_id_column": "building_id", "id": building_id},
    )
    if not len(lot_ids):
        print("no lot to process")
        return

    lot_thematiques = firestore_helper.search_thematic(
        {
            "resource_id": lot_ids,
            "scope": "lot",
            "version_name": version.get("version_name"),
            "version_date": version.get("version_date"),
            "thematique_name": version.get("thematique_name"),
        },
        firestore_client,
    )
    print("no example yet")


def process_copro(copro_id, sql_engine, firestore_client, thematique, step):
    # get all buildings to fetch columns to add and update copro
    building_ids = sql_helper.get_children_ids(
        sql_engine,
        {"children_table": "building", "parent_id_column": "copro_id", "id": copro_id},
    )

    if not len(building_ids):
        print("no lot to process")
        return

    thematique_dict = thematique.to_dict()
    step_dict = step.to_dict()
    # fetching all building thematics for buildings of the copro
    building_thematiques = firestore_helper.search_thematic(
        {
            "resource_id": building_ids,
            "scope": "building",
            "version_name": thematique_dict.get("version_name"),
            "version_date": thematique_dict.get("version_date"),
            "thematique_name": thematique_dict.get("thematique_name"),
        },
        firestore_client,
    )
    # init of the count of the fields to add and update
    count = building_fields[step_dict.get("metadata").get("name")]

    for bt in building_thematiques:
        # for each building, add the fields of the updated step to the count
        building_step = (
            firestore_client.collection("thematiques")
            .document(bt.id)
            .collection("steps")
            .where("metadata.name", "==", step_dict.get("metadata").get("name"))
        ).get()
        if len(building_step) == 0:
            print(f"step {step_dict.get('metadata').get('name')} not found")
            continue
        building_step = building_step[0]
        count = update_count(building_step.get("fields"), count)
        copro_thematique = firestore_helper.search_thematic(
            {
                "scope": "copro",
                "resource_id": copro_id,
                "version_name": thematique_dict.get("version_name"),
                "version_date": thematique_dict.get("version_date"),
                "thematique_name": thematique_dict.get("thematique_name"),
            },
            firestore_client,
        )
        if not len(copro_thematique):
            print("thematique for copro not found")
            return
        step = firestore_helper.search_step(
            copro_thematique[0], step_dict.get("metadata").get("name")
        )
        if not len(step):
            print(
                f"{step_dict.get('metadata').get('name')}: step not found for copro {copro_id}"
            )
            return
        update_payload = get_update_payload(step[0].get("fields"), count)
        print()


def update_count(fields, count):
    for field_name, field_item in fields.items():
        if field_item.get("type") == "group":
            for v in field_item.get("value"):
                count = update_count(v, count)
        if field_name in count:
            value = field_item.get("value", [0])
            if len(value) == 0:
                continue
            count[field_name] += value[0]
    return count


def get_update_payload(fields, changes):
    for field_name, field_item in fields.items():
        if field_item.get("type") == "group":
            for idx, v in enumerate(field_item.get("value")):
                field_item["value"][idx] = get_update_payload(v, changes)
        if field_name in changes:
            field_item["value"] = [changes[field_name]]
            field_item["disabled"] = True
    return fields


def process_subitems(
    child_scope,
    parent_scope,
    parent_id,
    parent_field,
    sql_engine,
    firestore_client,
    thematique,
    step,
):
    # get all subitems (lot for building, building for copro) to fetch columns to add and update parent
    subitem_ids = sql_helper.get_children_ids(
        sql_engine,
        {
            "children_table": child_scope,
            "parent_id_column": parent_field,
            "id": parent_id,
        },
    )

    if not len(subitem_ids):
        print(f"no {child_scope} to process")
        return

    thematique_dict = thematique.to_dict()
    step_dict = step.to_dict()
    # fetching all children thematics for children of the parent
    # children (subitem_ids) are list of children from SQL
    children_thematiques = firestore_helper.search_thematic(
        {
            "resource_id": subitem_ids,
            "scope": child_scope,
            "version_name": thematique_dict.get("version_name"),
            "version_date": thematique_dict.get("version_date"),
            "thematique_name": thematique_dict.get("thematique_name"),
        },
        firestore_client,
    )
    # init of the count of the fields to add and update
    if child_scope == "building":
        count = building_fields[step_dict.get("metadata").get("name")]
    else:
        count = lot_fields[step_dict.get("metadata").get("name")]

    update_payload = {
        "fields": {}
    }
    for child_thematique in children_thematiques:
        # for each children thematique, add the fields of the updated step to the count
        # first find the correspondant step for the current thematique
        child_step = (
            firestore_client.collection("thematiques")
            .document(child_thematique.id)
            .collection("steps")
            .where("metadata.name", "==", step_dict.get("metadata").get("name"))
        ).get()
        if len(child_step) == 0:
            print(f"step {step_dict.get('metadata').get('name')} not found")
            continue
        # child_step is an array, but a thematic can only have each step once
        child_step = child_step[0]
        count = update_count(child_step.get("fields"), count)

    update_payload = find_parent_step(
        parent_scope=parent_scope,
        parent_id=parent_id,
        firestore_client=firestore_client,
        thematique_dict=thematique_dict,
        step_name=step_dict.get('metadata').get('name')
    )

    update_payload["fields"] = get_update_payload(
        update_payload["fields"], count)
    firestore_helper.update_item(
        {
            "resource_id": parent_id,
            "scope": parent_scope,
            "version_name": thematique_dict.get("version_name"),
            "version_date": thematique_dict.get("version_date"),
            "thematique_name": thematique_dict.get("thematique_name"),
        },
        step_dict.get('metadata').get('name'),
        update_payload,
        firestore_client
    )


def find_parent_step(parent_scope, parent_id, thematique_dict, firestore_client, step_name):
    parent_thematique = firestore_helper.search_thematic(
        {
            "scope": parent_scope,
            "resource_id": parent_id,
            "version_name": thematique_dict.get("version_name"),
            "version_date": thematique_dict.get("version_date"),
            "thematique_name": thematique_dict.get("thematique_name"),
        },
        firestore_client,
    )
    if not len(parent_thematique):
        print(f"thematique for {parent_scope} not found")
        return
    step = firestore_helper.search_step(
        parent_thematique[0], step_name
    )
    if not len(step):
        print(
            f"{step_name}: step not found for {parent_scope} {parent_id}"
        )
        return
    return step[0].to_dict()
