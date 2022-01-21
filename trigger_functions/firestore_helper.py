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
