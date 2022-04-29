import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        # "projectId": "app-oslo-dev",
        "projectId": "app-oslo-preprod",
    },
)
db = firestore.client()

thematiques = [
    "SITUATION_JURIDIQUE_FONCIER",
    "OCCUPATION_SOCIALE",
    "CHARGES",
    "IMPAYES",
]
scopes = ["sc", "copro", "building", "lot"]
collections = ["thematiques_template", "thematiques"]

for collection_name in collections:
    collection = db.collection(collection_name)
    for thematique_name in thematiques:
        thematique_exists = collection.where(
            "thematique_name", "==", thematique_name
        ).stream()
        for existing in thematique_exists:
            scope = existing.get("scope")
            res = scopes.index(scope)
            if res >= 0:
                print(f"collection {collection_name} |   scope {scope} |  thematic {thematique_name}")
                collection.document(existing.id).delete()
