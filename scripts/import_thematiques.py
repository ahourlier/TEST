import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {"projectId": "app-oslo-dev",})
db = firestore.client()

folder_name = "thematiques"
thematique_template_collection = "thematiques_template"
step_collection = "steps"

for filename in os.listdir(folder_name):

    with open(f"{folder_name}/{filename}") as f:
        thematique_data = json.load(f)

    thematique_exists = (
        db.collection(thematique_template_collection)
        .where("thematique_name", "==", thematique_data.get("thematique_name"))
        .where("scope", "==", thematique_data.get("scope"))
        .get()
    )

    if len(thematique_exists) > 0:
        for existing in thematique_exists:
            db.collection(thematique_template_collection).document(existing.id).delete()

    steps = thematique_data.get("steps")
    del thematique_data["steps"]
    created_thematique = db.collection(thematique_template_collection).document()
    created_thematique.set(thematique_data)

    for step in steps:
        current_step = created_thematique.collection(step_collection).document()
        current_step.set(step)

    print(f"done for {filename}")
