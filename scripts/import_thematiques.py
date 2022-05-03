import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import csv
import os

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

DRY_RUN = False

i18n_keys = []

thematique_template_collection = "thematiques_template"
step_collection = "steps"


def handle_step_fields(fields_object, thematique_name, step_name):
    for idx, field_name in enumerate(fields_object.keys()):
        fields_object[field_name][
            "label"
        ] = f"thematic.{thematique_name}.{step_name}.fields.{field_name}"
        fields_object[field_name]["order"] = idx + 1
        if fields_object[field_name]["label"] not in i18n_keys:
            i18n_keys.append(fields_object[field_name]["label"])
        if fields_object[field_name].get("type") == "group":
            fields_object[field_name]["value"][0] = handle_step_fields(
                fields_object[field_name]["value"][0], thematique_name, step_name
            )
    return fields_object


folders = [
    "thematiques/T2",
    "thematiques/T3",
    "thematiques/T5",
    "thematiques/T6",
]
for folder_name in folders:
    for filename in os.listdir(folder_name):

        with open(f"{folder_name}/{filename}") as f:
            thematique_data = json.load(f)
        thematique_name = thematique_data["thematique_name"]
        thematique_exists = (
            db.collection(thematique_template_collection)
            .where("thematique_name", "==", thematique_name)
            .where("scope", "==", thematique_data.get("scope"))
            .get()
        )

        if len(thematique_exists) > 0:
            print(f"found {len(thematique_exists)} thematics to delete")
            for existing in thematique_exists:
                if not DRY_RUN:
                    db.collection(thematique_template_collection).document(
                        existing.id
                    ).delete()

        steps = thematique_data.get("steps")
        del thematique_data["steps"]
        thematique_data["label"] = f"thematic.{thematique_name}.name"

        if thematique_data["label"] not in i18n_keys:
            i18n_keys.append(thematique_data["label"])

        if not DRY_RUN:
            created_thematique = db.collection(
                thematique_template_collection
            ).document()
            created_thematique.set(thematique_data)

        for step in steps:
            step["fields"]["commentaire"] = {
                "type": "textArea",
                "multiple": False,
                "lg": 12,
                "value": [],
            }
            step_name = step["metadata"]["name"]
            step["fields"] = handle_step_fields(
                step.get("fields"), thematique_name, step_name
            )

            step["metadata"]["label"] = f"thematic.{thematique_name}.{step_name}.name"

            if step["metadata"]["label"] not in i18n_keys:
                i18n_keys.append(step["metadata"]["label"])

            if not DRY_RUN:
                current_step = created_thematique.collection(step_collection).document()
                current_step.set(step)

        with open("new_keys.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(map(lambda key: [key], i18n_keys))
        print(f"done for {filename}")
