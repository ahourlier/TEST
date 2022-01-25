def get_ids_from_context(context):
    path_parts = context.resource.split("/documents/")[1].split("/")
    thematique_id = path_parts[1]
    step_id = path_parts[3]
    return thematique_id, step_id


def search_thematic(params: dict, db):
    query = db.collection("thematiques")

    for key, value in params.items():
        if type(value) == list:
            query = query.where(key, "in", value)
        else:
            query = query.where(key, "==", value)

    return query.get()


def search_step(thematique_document, step_name):
    return (
        thematique_document.reference.collection("steps")
        .where("metadata.name", "==", step_name)
        .get()
    )


def update_item(version_details, step_name, changes, firestore_client):
    thematics_found = search_thematic(version_details, firestore_client)
    if not len(thematics_found):
        print("thematic not found with these details")
        print(version_details)

    step = search_step(thematics_found[0], step_name=step_name)
    if not len(thematics_found):
        print(f"{step_name} not found in thematic with these details")
        print(version_details)
    
    step = step[0]
    step.reference.set(
        changes,
        merge=True
    )