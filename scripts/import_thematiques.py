import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import csv
import os

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {"projectId": "app-oslo-dev",})
db = firestore.client()

i18n_keys = []

folder_name = "thematiques"
thematique_template_collection = "thematiques_template"
step_collection = "steps"


def handle_step_fields(fields_object):
    for idx, field_name in enumerate(fields_object.keys()):
        fields_object[field_name]["label"] = f"thematic.fields.{field_name}"
        fields_object[field_name]["order"] = idx + 1
        if fields_object[field_name]["label"] not in i18n_keys:
            i18n_keys.append(fields_object[field_name]["label"])
        if fields_object[field_name].get("type") == "group":
            fields_object[field_name]["value"][0] = handle_step_fields(
                fields_object[field_name]["value"][0]
            )
    return fields_object


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
    thematique_data["label"] = f"thematic.name.{thematique_data['thematique_name']}"

    if thematique_data["label"] not in i18n_keys:
        i18n_keys.append(thematique_data["label"])

    created_thematique = db.collection(thematique_template_collection).document()
    created_thematique.set(thematique_data)

    for step in steps:
        step["fields"] = handle_step_fields(step.get("fields"))

        step["metadata"]["label"] = f"thematic.step.{step['metadata']['name']}"

        if step["metadata"]["label"] not in i18n_keys:
            i18n_keys.append(step["metadata"]["label"])

        current_step = created_thematique.collection(step_collection).document()
        current_step.set(step)

    with open("new_keys.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(map(lambda key: [key], i18n_keys))
    print(f"done for {filename}")
