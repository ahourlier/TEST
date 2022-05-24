from flask import request
from app import db
from time import sleep
import logging
import traceback
from app.common.sheets_util import SheetsUtils
from app.v2_imports.model import Imports, ImportStatus, ImportType
from app.internal_api.base import InternalAPIView


class ImportRunView(InternalAPIView):
    def put(self):
        from app.v2_imports.copros.process import CoproImport
        from app.v2_imports.lots.process import LotImport

        payload = request.get_json(force=True)
        running_import = Imports.query.get(payload.get("import_id"))
        if not running_import:
            print(f"import {payload.get('import_id')} not found")
            return f"import {payload.get('import_id')} not found"

        A1_notation_filters = ""
        if running_import.import_type == "liste d'adresses d'immeubles":
            A1_notation_filters = "A:J"
        elif (
            running_import.import_type
            == "équivalent d'une feuille de présence par adresse"
        ):
            A1_notation_filters = "A:S"
        else:
            return f"Unknown import: check import_type names"

        try:
            data = SheetsUtils.get_spreadsheet_by_datafilter(
                spreasheet_id=running_import.import_sheet_id,
                A1_notation_filters=[],
                user_email=payload.get("email"),
            )
            data = SheetsUtils.format_sheet(data)
            sheet_found = False
            for key in data:
                if key == "DATA":
                    sheet_found = True
                    data = data[key]
            if not sheet_found:
                raise Exception("No sheet with 'DATA' name found... Please rename the sheet")
        except Exception as e:
            print(traceback.format_exc())
            running_import.status = ImportStatus.ERROR.value
            db.session.commit()
            return f"An error occurred reading import spreadsheet"

        try:
            if running_import.import_type == "liste d'adresses d'immeubles":
                CoproImport.run_copro_import(
                    running_import,
                    dry_run=running_import.type == ImportType.SCAN.value,
                    data=data,
                    A1_notation_filters=A1_notation_filters,
                    user_email=payload.get("email"),
                )
            elif (
                running_import.import_type
                == "équivalent d'une feuille de présence par adresse"
            ):
                LotImport.run_lot_import(
                    running_import,
                    dry_run=running_import.type == ImportType.SCAN.value,
                    data=data,
                    A1_notation_filters=A1_notation_filters,
                    user_email=payload.get("email"),
                )
        except Exception:
            logging.error(f"an error occurred when running import {running_import.id}")
            print(traceback.format_exc())
            running_import.status = ImportStatus.ERROR.value
            db.session.commit()
            return "done with errors"
        sleep(5)
        running_import.status = ImportStatus.DONE.value
        db.session.commit()
        return "done"
