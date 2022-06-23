from services.firestore import FirestoreUtils
from services.thematiques import process_template


def run_export(request):
    """
    Export thematiques from Firestore in BQ for reporting
    @params: request: HTTP request from Cloud Functions
    """
    firestore_utils = FirestoreUtils()
    # fetch all templates
    templates = firestore_utils.list_templates()
    # for each template, process all entities with this template
    for template in templates:
        process_template(template, firestore_utils)



run_export(None)
