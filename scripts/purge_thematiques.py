import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials

GCP_PROJECT = {
    "projectId": "app-oslo-dev",
    # "projectId": "app-oslo-preprod",
    # "projectId": "app-oslo-prod",
}

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, GCP_PROJECT)
db = firestore.client()

if __name__ == "__main__":
    delete = True

    if (
        GCP_PROJECT["projectId"] == "app-oslo-prod"
        or GCP_PROJECT["projectId"] == "app-oslo-preprod"
    ):
        delete = False
        resp = input(
            f"WARNING: You're going to delete all firestore data inside {GCP_PROJECT['projectId']}:\n\nConfirm? [y/N] "
        )
        if resp == "y" or resp == "Y":
            delete = True
        else:
            print("Aborting...")
            exit(0)

    if delete == True:
        thematiques = [
            "ENVIRONNEMENT_URBAIN_CADRE_VIE",  # T1
            "SITUATION_JURIDIQUE_FONCIER",  # T2
            "OCCUPATION_SOCIALE",  # T3
            "GESTION_ET_FONCTIONNEMENT",  # T4
            "CHARGES",  # T5
            "IMPAYES",  # T6
            "EQUIPEMENT_ET_BATI",  # T7
            "SUIVI_FINANCEMENTS_PC_ET_PPIC",  # T8
            "SUIVI_FINANCEMENTS_PP",  # T9
            "POSITIONNEMENT_IMMOBILIER",  # T10
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
                        print(
                            f"COLLECTION {collection_name}   |  THEMATIC {thematique_name}    |   SCOPE {scope}"
                        )
                        existing.reference.delete()
                        collection.document(existing.id).delete()
