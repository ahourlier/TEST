from app.common.api import AuthenticatedApi
from flask_accepts import accepts, responds
from flask import request, jsonify, Response

from . import api, FinancialDevice
from .schema import FinancialDeviceSchema, FinancialDeviceUpdateSchema
from .service import FinancialDeviceService


@api.route("")
class FinancialDeviceResource(AuthenticatedApi):
    @accepts(schema=FinancialDeviceSchema, api=api)
    @responds(schema=FinancialDeviceSchema, api=api)
    def post(self):
        return FinancialDeviceService.create(request.parsed_obj)


@api.route("/<int:financial_device_id>")
@api.param("financial_deviceId", "FinancialDevice unique ID")
class FinancialDeviceResource(AuthenticatedApi):
    @accepts(schema=FinancialDeviceSchema, api=api)
    @responds(schema=FinancialDeviceSchema, api=api)
    def get_by_mission_detail_id(self, mission_detail_id):
        return FinancialDeviceService.get_by_mission_detail_id(mission_detail_id)

    @accepts(schema=FinancialDeviceUpdateSchema, api=api)
    @responds(schema=FinancialDeviceSchema, api=api)
    def put(self, financial_device_id: int):
        db_financial_device = FinancialDeviceService.get_by_id(financial_device_id)
        return FinancialDeviceService.update(db_financial_device, request.parsed_obj)

    def delete(self, financial_device_id: int) -> Response:
        id = FinancialDeviceService.delete(financial_device_id)
        return jsonify(dict(status="Success", id=id))
