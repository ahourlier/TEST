from app import db

from app.mission.missions.mission_details.financial_device.error_handlers import (
    FinancialDeviceNotFoundException,
)
from app.mission.missions.mission_details.financial_device.model import FinancialDevice
from app.mission.missions.mission_details.service import MissionDetailService


class FinancialDeviceService:
    @staticmethod
    def create(financial_device):
        new_financial_device = FinancialDevice(**financial_device)
        db.session.add(new_financial_device)
        db.session.commit()
        return new_financial_device

    @staticmethod
    def get_by_id(financial_device_id: int):
        financial_device = FinancialDevice.query.get(financial_device_id)
        if not financial_device:
            raise FinancialDeviceNotFoundException
        return financial_device

    @staticmethod
    def get_by_mission_detail_id(mission_detail_id: int):
        financial_device = FinancialDevice.query.filter(FinancialDevice.mission_details_id == mission_detail_id).first()
        if not financial_device:
            raise FinancialDeviceNotFoundException
        return financial_device

    @staticmethod
    def update(db_financial_device: FinancialDevice, new_attrs):
        if "mission_details_id" in new_attrs:
            MissionDetailService.get_by_id(new_attrs["mission_details_id"])

        db_financial_device.update(new_attrs)
        db.session.commit()
        return db_financial_device

    @staticmethod
    def delete(financial_device_id):
        financial_device = FinancialDevice.query.filter(FinancialDevice.id == financial_device_id).first()

        if not financial_device:
            raise FinancialDeviceNotFoundException

        db.session.delete(financial_device)
        db.session.commit()
        return financial_device_id
