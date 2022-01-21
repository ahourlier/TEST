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


class FakeContext:
    resource = "/documents/thematiques/5650mrcmdjFykPgCyc2Z/steps/vuWIXSsaRPaQ2ZmgNgF5"


def on_update(data, context):
    """Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    thematique_id, step_id = firestore_helper.get_ids_from_context(context)
    thematique = client.collection("thematiques").document(thematique_id).get()
    step = client.document(f"thematiques/{thematique_id}/steps/{step_id}").get()

    if not thematique.exists:
        print(f"document with id {thematique_id} not found")
        return "document not found"

    thematique_dict = thematique.to_dict()

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
    if item.get("building_id"):
        # if updated item has a building id, updating its building in firestore
        # thematics_helper.process_building(
        #     item.get("building_id"), engine, client, thematique_dict
        # )
        thematics_helper.process_subitems(
            child_scope="lot",
            parent_scope="building",
            parent_id=item.get("building_id"),
            parent_field="building_id",
            sql_engine=engine,
            firestore_client=client,
            thematique=thematique,
            step=step,
        )

    if item.get("copro_id"):
        # if updated item has a copro id, updating its copro in firestore
        thematics_helper.process_subitems(
            child_scope="building",
            parent_scope="copro",
            parent_id=item.get("copro_id"),
            parent_field="copro_id",
            sql_engine=engine,
            firestore_client=client,
            thematique=thematique,
            step=step,
        )
    print()


on_update(
    {
        "metadata": {
            "legendes": [],
            "label": "thematic.step.DECOMPOSITION_DEPENSE",
            "status": "",
            "id": "vuWIXSsaRPaQ2ZmgNgF5",
            "order": 1,
            "name": "DECOMPOSITION_DEPENSE",
        },
        "fields": {
            "campagne_travaux": {
                "multiple": True,
                "type": "group",
                "order": 1,
                "label": "thematic.fields.campagne_travaux",
                "value": [
                    {
                        "frais_cumule_pc_ppic_ht": {
                            "label": "thematic.fields.frais_cumule_pc_ppic_ht",
                            "type": "number",
                            "multiple": False,
                            "value": [],
                            "order": 15,
                        },
                        "nature_travaux_pc": {
                            "type": "select_multiple",
                            "endpoint": "/referential/enums/?enums=NatureTravauxPartieCommune",
                            "value": [],
                            "label": "thematic.fields.nature_travaux_pc",
                            "order": 6,
                            "multiple": False,
                        },
                        "depense_subventionnable_pc_ppic_ht": {
                            "type": "number",
                            "label": "thematic.fields.depense_subventionnable_pc_ppic_ht",
                            "value": [],
                            "multiple": False,
                            "order": 17,
                        },
                        "depense_totale_pc_ppic_ttc": {
                            "multiple": False,
                            "value": [],
                            "type": "number",
                            "order": 18,
                            "label": "thematic.fields.depense_totale_pc_ppic_ttc",
                        },
                        "depense_totale_pc_ttc": {
                            "order": 12,
                            "multiple": False,
                            "type": "number",
                            "label": "thematic.fields.depense_totale_pc_ttc",
                            "value": [],
                        },
                        "travaux_cumule_pc_ppic_ttc": {
                            "label": "thematic.fields.travaux_cumule_pc_ppic_ttc",
                            "type": "number",
                            "multiple": False,
                            "value": [],
                            "order": 14,
                        },
                        "entreprise_1_poste_plus_couteux": {
                            "value": [],
                            "multiple": False,
                            "order": 3,
                            "label": "thematic.fields.entreprise_1_poste_plus_couteux",
                            "type": "string",
                        },
                        "travaux_pc_ttc": {
                            "label": "thematic.fields.travaux_pc_ttc",
                            "multiple": False,
                            "type": "number",
                            "value": [],
                            "order": 8,
                        },
                        "nom_campagne_travaux": {
                            "label": "thematic.fields.nom_campagne_travaux",
                            "type": "string",
                            "value": [],
                            "order": 1,
                            "multiple": False,
                        },
                        "date_vote_ag": {
                            "multiple": False,
                            "label": "thematic.fields.date_vote_ag",
                            "type": "date",
                            "value": [],
                            "order": 2,
                        },
                        "entreprise_2_poste_plus_couteux": {
                            "label": "thematic.fields.entreprise_2_poste_plus_couteux",
                            "type": "string",
                            "value": [],
                            "order": 4,
                            "multiple": False,
                        },
                        "depense_subventionnable_pc_ht": {
                            "type": "number",
                            "label": "thematic.fields.depense_subventionnable_pc_ht",
                            "order": 11,
                            "value": [],
                            "multiple": False,
                        },
                        "frais_pc_ttc": {
                            "multiple": False,
                            "type": "number",
                            "value": [],
                            "order": 10,
                            "label": "thematic.fields.frais_pc_ttc",
                        },
                        "travaux_cumule_pc_ppic_ht": {
                            "multiple": False,
                            "order": 13,
                            "type": "number",
                            "label": "thematic.fields.travaux_cumule_pc_ppic_ht",
                            "value": [],
                        },
                        "travaux_pc_ht": {
                            "order": 7,
                            "value": [],
                            "multiple": False,
                            "label": "thematic.fields.travaux_pc_ht",
                            "type": "number",
                        },
                        "frais_pc_ht": {
                            "value": [],
                            "order": 9,
                            "multiple": False,
                            "label": "thematic.fields.frais_pc_ht",
                            "type": "number",
                        },
                        "entreprise_3_poste_plus_couteux": {
                            "type": "string",
                            "value": [],
                            "label": "thematic.fields.entreprise_3_poste_plus_couteux",
                            "order": 5,
                            "multiple": False,
                        },
                        "frais_cumule_pc_ppic_ttc": {
                            "type": "number",
                            "value": [],
                            "label": "thematic.fields.frais_cumule_pc_ppic_ttc",
                            "order": 16,
                            "multiple": False,
                        },
                    }
                ],
            },
            "commentaire": {
                "label": "thematic.fields.commentaire",
                "order": 2,
                "type": "textArea",
                "multiple": False,
                "value": [],
            },
        },
    },
    FakeContext(),
)
