from google.cloud import firestore

client = firestore.Client()


def on_update(data, context):
    """ Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    path_parts = context.resource.split("/documents/")[1].split("/")
    thematique_id = path_parts[1]
    step_id = path_parts[3]
