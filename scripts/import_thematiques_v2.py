import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from copy import deepcopy
import json
import csv
import os

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        "projectId": "app-oslo-dev",
        # "projectId": "app-oslo-preprod",
    },
)
db = firestore.client()

DRY_RUN = False

i18n_keys = []

thematique_template_collection = "thematiques_template"
step_collection = "steps"


def get_fields(fields, thematique_name, step_name, scope):
    fields_obj = {}
    for idx, field_name in enumerate(fields.keys()):
        field_scopes = ["sc", "copro", "building", "lot"]
        if not DRY_RUN:
            field_scopes = fields[field_name]["scopes"]
        if scope in field_scopes:
            field = deepcopy(fields[field_name])
            del field["scopes"]
            field["scope"] = scope
            field["order"] = idx + 1
            label = f"thematic.{thematique_name}.{step_name}.fields.{field_name}"
            if field_name == "default_group":
                label = f"thematic.{thematique_name}.{step_name}.name"
            if label not in i18n_keys:
                i18n_keys.append(label)
            field["label"] = label
            if field["type"] == "group":
                field["value"][0] = get_fields(
                    field["value"][0],
                    thematique_name,
                    step_name,
                    scope,
                )
                if field_name != "default_group":
                    i18n_keys.append("")
            fields_obj[field_name] = field
    return fields_obj


thematique_files = [
    "T1",
    "T2",
    "T3",
    "T4",
    "T5",
    "T6",
    "T7",
    "T8",
    "T9",
    "T10",
]
for file_name in thematique_files:
    with open(f"thematiques/{file_name}.json") as f:
        thematique_data = json.load(f)
    thematique_name = thematique_data["thematique_name"]
    scopes = ["sc"]
    if not DRY_RUN:
        scopes = thematique_data["scopes"]
    del thematique_data["scopes"]
    versionnable = thematique_data["versionnable"]
    heritable = thematique_data["heritable"]
    extend_parent = thematique_data["extend_parent"]
    steps = thematique_data["steps"]
    thematique_label = f"thematic.{thematique_name}.name"
    thematique_data["label"] = thematique_label
    if thematique_label not in i18n_keys:
        i18n_keys.append(thematique_label)
    i18n_keys.append("")
    i18n_keys.append("")
    for idx, scope in enumerate(scopes):
        thematique_exists = (
            db.collection(thematique_template_collection)
            .where("thematique_name", "==", thematique_name)
            .where("scope", "==", scope)
            .get()
        )
        if len(thematique_exists) > 0:
            print(f"found {len(thematique_exists)} thematics to delete")
            for existing in thematique_exists:
                if not DRY_RUN:
                    db.collection(thematique_template_collection).document(
                        existing.id
                    ).delete()
        if not DRY_RUN:
            thematique_data["scope"] = scope
            thematique_data["versionnable"] = versionnable[idx]
            thematique_data["heritable"] = heritable[idx]
            thematique_data["extend_parent"] = extend_parent[idx]
            thematique_data.pop("steps", None)
        if not DRY_RUN:
            created_thematique = db.collection(
                thematique_template_collection
            ).document()
            created_thematique.set(thematique_data)
        for step_idx, step in enumerate(steps):
            step_data = deepcopy(step)
            step_scopes = ["sc", "copro", "building", "lot"]
            if not DRY_RUN:
                step_scopes = step_data["metadata"]["scopes"]
            if scope in step_scopes:
                step_name = step_data["metadata"]["name"]
                step_label = f"thematic.{thematique_name}.{step_name}.name"
                step_data["metadata"]["order"] = step_idx + 1
                step_data["metadata"]["label"] = step_label
                if step_label not in i18n_keys:
                    i18n_keys.append(step_label)
                step_data["fields"] = get_fields(
                    step_data["fields"], thematique_name, step_name, scope
                )
                if not DRY_RUN:
                    step_data["fields"]["commentaire"] = {
                        "type": "textArea",
                        "label": "common.label.comment",
                        "multiple": False,
                        "order": 1000,
                        "lg": 12,
                        "scope": ["sc", "copro", "building", "lot"],
                        "value": [],
                    }
                    current_step = created_thematique.collection(
                        step_collection
                    ).document()
                    current_step.set(step_data)
        with open("new_keys.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(map(lambda key: [key], i18n_keys))
        print(f"DONE FOR {thematique_name}    |    SCOPE {scope}")
