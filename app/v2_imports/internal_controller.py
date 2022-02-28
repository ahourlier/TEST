from flask import request
from app import db
from time import sleep
from app.v2_imports.model import Imports, ImportStatus
from app.internal_api.base import InternalAPIView


class ImportRunView(InternalAPIView):
    def put(self):
        payload = request.get_json(force=True)
        running_import = Imports.query.get(payload.get("import_id"))
        if not running_import:
            print(f"import {payload.get('import_id')} not found")
            return f"import {payload.get('import_id')} not found"
        sleep(5)
        running_import.status = ImportStatus.DONE.value
        db.session.commit()
        return "done"
