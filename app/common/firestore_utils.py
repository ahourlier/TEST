from firebase_admin import firestore


class FirestoreUtils:
    def __init__(self):
        self.client = firestore.client()

    def list_items(self, collection):
        return self.client.collection(collection).get()
