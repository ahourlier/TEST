from google.cloud import firestore
from dotenv import dotenv_values
from sqlalchemy import create_engine, text, MetaData

import sql_helper
import firestore_helper
import thematics_helper


CONFIG = dotenv_values(".env")
client = firestore.Client(project=CONFIG.get("GOOGLE_CLOUD_PROJECT"))
engine = create_engine(CONFIG.get("SQLALCHEMY_DATABASE_URI"))
metadata = MetaData(bind=engine, schema="core")
metadata.reflect(bind=engine)

# Used for local tests
# class FakeContext:
#     resource = "/documents/thematiques/ALxVaWH4yKjyfagrSPVu/steps/evIAYa52ye77MUyEWQVG"

# Deployed function on Cloud function
# Called for each step update
def on_update(data, context):

    thematique_id, step_id = firestore_helper.get_ids_from_context(context)
    thematique = client.collection("thematiques").document(thematique_id).get()

    if not thematique.exists:
        print(f"document with id {thematique_id} not found")
        return f"document with id {thematique_id} not found"

    step = client.document(f"thematiques/{thematique_id}/steps/{step_id}").get()

    if not step.exists:
        print(f"step not found for id '{step_id}'")
        return f"step not found for id '{step_id}'"

    thematique_dict = thematique.to_dict()

    # Need only upward updates
    if thematique_dict.get("scope") == "copro":
        print("scope is copro, not calculating")
        return "scope is copro, not calculating"

    params = {
        "table": thematique_dict.get("scope"),
        "id": thematique_dict.get("resource_id"),
        "columns": ["id", "copro_id"],
    }
    if thematique_dict.get("scope") == "lot":
        params["columns"].append("building_id")

    # getting item that was updated
    item = sql_helper.get_item(engine, params)

    if not item:
        print(f"item with params {params} was not found")
        return f"item with params {params} was not found"

    # If item is a lot, process its building
    if item.get("building_id"):
        # Update parent (building)
        thematics_helper.process_subitems(
            child_scope="lot",
            parent_scope="building",
            parent_id=item.get("building_id"),
            parent_field="building_id",
            sql_engine=engine,
            firestore_client=client,
            thematique_dict=thematique_dict,
            step_dict=step.to_dict(),
        )
    # If item is a building or lot
    if item.get("copro_id"):
        # Update parent (copro or building)
        thematics_helper.process_subitems(
            child_scope="building",
            parent_scope="copro",
            parent_id=item.get("copro_id"),
            parent_field="copro_id",
            sql_engine=engine,
            firestore_client=client,
            thematique_dict=thematique_dict,
            step_dict=step.to_dict(),
        )
