from flask import request
from app import db
from time import sleep
import logging
from app.v2_imports.model import Imports, ImportStatus, ImportType
from app.internal_api.base import InternalAPIView


class ImportRunView(InternalAPIView):
    def put(self):
        from app.v2_imports.service import ImportsService

        payload = request.get_json(force=True)
        running_import = Imports.query.get(payload.get("import_id"))
        if not running_import:
            print(f"import {payload.get('import_id')} not found")
            return f"import {payload.get('import_id')} not found"

        try:
            if running_import.import_type == "liste d'adresses d'immeubles":
                ImportsService.run_copro_import(
                    running_import,
                    dry_run=running_import.type == ImportType.SCAN.value,
                )
            elif (
                running_import.import_type
                == "équivalent d'une feuille de présence par adresse"
            ):
                ImportsService.run_lot_import(
                    running_import,
                    dry_run=running_import.type == ImportType.SCAN.value,
                )
        except Exception as e:
            logging.error(f"an error occurred when running import {running_import.id}")
            logging.error(e)
            running_import.status = ImportStatus.ERROR.value
            db.session.commit()
            return "done with errors"
        sleep(5)
        running_import.status = ImportStatus.DONE.value
        db.session.commit()
        return "done"
