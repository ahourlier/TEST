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
    resource = "/documents/thematiques/CSf79kgd0Onkfhs9V5L4/steps/Byi1Aofu3LH08ZqujyQb"


def on_update(data, context):

    thematique_id, step_id = firestore_helper.get_ids_from_context(context)
    thematique = client.collection("thematiques").document(thematique_id).get()

    if not thematique.exists:
        print(f"document with id {thematique_id} not found")
        return f"document with id {thematique_id} not found"

    step = client.document(
        f"thematiques/{thematique_id}/steps/{step_id}").get()
    
    if not step.exists:
        print(f"step not found for id '{step_id}'")
        return f"step not found for id '{step_id}'"

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

    if not item:
        print(f"item with params {params} was not found")
        return f"item with params {params} was not found"

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


on_update(
    {
        "fields": {
            "campagne_travaux": {
                "label": "thematic.fields.campagne_travaux",
                "order": 1,
                "value": [
                    {
                        "travaux_pc_ttc": {
                            "label": "thematic.fields.travaux_pc_ttc",
                            "value": [
                                500
                            ],
                            "order": 8,
                            "multiple": False,
                            "type": "number"
                        },
                        "date_vote_ag": {
                            "multiple": False,
                            "order": 2,
                            "value": [],
                            "type": "date",
                            "label": "thematic.fields.date_vote_ag"
                        },
                        "travaux_pc_ht": {
                            "multiple": False,
                            "type": "number",
                            "label": "thematic.fields.travaux_pc_ht",
                            "order": 7,
                            "value": [
                                300
                            ]
                        },
                        "depense_subventionnable_pc_ht": {
                            "value": [
                                15
                            ],
                            "label": "thematic.fields.depense_subventionnable_pc_ht",
                            "multiple": False,
                            "order": 11,
                            "type": "number"
                        },
                        "depense_subventionnable_pc_ppic_ht": {
                            "value": [],
                            "type": "number",
                            "label": "thematic.fields.depense_subventionnable_pc_ppic_ht",
                            "multiple": False,
                            "order": 17
                        },
                        "travaux_cumule_pc_ppic_ttc": {
                            "multiple": False,
                            "type": "number",
                            "order": 14,
                            "value": [],
                            "label": "thematic.fields.travaux_cumule_pc_ppic_ttc"
                        },
                        "entreprise_3_poste_plus_couteux": {
                            "type": "string",
                            "value": [],
                            "label": "thematic.fields.entreprise_3_poste_plus_couteux",
                            "multiple": False,
                            "order": 5
                        },
                        "entreprise_1_poste_plus_couteux": {
                            "label": "thematic.fields.entreprise_1_poste_plus_couteux",
                            "type": "string",
                            "order": 3,
                            "multiple": False,
                            "value": []
                        },
                        "frais_cumule_pc_ppic_ttc": {
                            "type": "number",
                            "multiple": False,
                            "label": "thematic.fields.frais_cumule_pc_ppic_ttc",
                            "order": 16,
                            "value": []
                        },
                        "frais_pc_ht": {
                            "multiple": False,
                            "label": "thematic.fields.frais_pc_ht",
                            "type": "number",
                            "order": 9,
                            "value": [
                                50
                            ]
                        },
                        "depense_totale_pc_ppic_ttc": {
                            "order": 18,
                            "multiple": False,
                            "type": "number",
                            "value": [],
                            "label": "thematic.fields.depense_totale_pc_ppic_ttc"
                        },
                        "depense_totale_pc_ttc": {
                            "value": [
                                20
                            ],
                            "multiple": False,
                            "order": 12,
                            "type": "number",
                            "label": "thematic.fields.depense_totale_pc_ttc"
                        },
                        "frais_pc_ttc": {
                            "order": 10,
                            "type": "number",
                            "label": "thematic.fields.frais_pc_ttc",
                            "multiple": False,
                            "value": [
                                75
                            ]
                        },
                        "frais_cumule_pc_ppic_ht": {
                            "order": 15,
                            "value": [],
                            "label": "thematic.fields.frais_cumule_pc_ppic_ht",
                            "type": "number",
                            "multiple": False
                        },
                        "entreprise_2_poste_plus_couteux": {
                            "order": 4,
                            "type": "string",
                            "value": [],
                            "multiple": False,
                            "label": "thematic.fields.entreprise_2_poste_plus_couteux"
                        },
                        "nom_campagne_travaux": {
                            "order": 1,
                            "label": "thematic.fields.nom_campagne_travaux",
                            "multiple": False,
                            "value": [],
                            "type": "string"
                        },
                        "travaux_cumule_pc_ppic_ht": {
                            "label": "thematic.fields.travaux_cumule_pc_ppic_ht",
                            "type": "number",
                            "value": [],
                            "order": 13,
                            "multiple": False
                        },
                        "nature_travaux_pc": {
                            "type": "select_multiple",
                            "multiple": False,
                            "value": [],
                            "label": "thematic.fields.nature_travaux_pc",
                            "endpoint": "/referential/enums/?enums=NatureTravauxPartieCommune",
                            "order": 6
                        }
                    }
                ],
                "type": "group",
                "multiple": True
            },
            "commentaire": {
                "value": [],
                "order": 2,
                "type": "textArea",
                "label": "thematic.fields.commentaire",
                "multiple": False
            }
        },
        "metadata": {
            "id": "Byi1Aofu3LH08ZqujyQb",
            "order": 1,
            "label": "thematic.step.TRAVAUX_VOTES_AG_DECOMPOSITION_DEPENSE",
            "legendes": [],
            "status": "",
            "name": "TRAVAUX_VOTES_AG_DECOMPOSITION_DEPENSE"
        }
    },
    FakeContext(),
)
