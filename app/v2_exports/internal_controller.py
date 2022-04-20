from flask import request
from app import db
from time import sleep
import logging
import traceback
from app.common.sheets_util import SheetsUtils
from app.v2_exports.model import Exports, ExportStatus
from app.internal_api.base import InternalAPIView


class ExportRunView(InternalAPIView):
    def put(self):
        # from app.v2_exports.copros.process import CoproExport
        # from app.v2_exports.lots.process import LotExport
        payload = request.get_json(force=True)
        print(payload)

        running_export = Exports.query.get(payload.get("export_id"))
        if not running_export:
            print(f"export {payload.get('export_id')} not found")
            return f"export {payload.get('export_id')} not found"
        return "done"