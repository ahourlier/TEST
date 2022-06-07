import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        "projectId": "app-oslo-dev",
    },
)
db = firestore.client()

thematics = db.collection("thematiques").get()

for d in thematics:
    try:
        print(f"treating thematic for {d.get('scope')} {d.get('resource_id')}")
    except Exception:
        pass
    steps = d.reference.collection("steps").get()
    for s in steps:
        s.reference.delete()
        try:
            print(f"deleted {d.get('label')}")
        except Exception:
            pass
    d.reference.delete()
    try:
        print(f"deleted thematic for {d.get('scope')} {d.get('resource_id')}")
    except Exception:
        pass
