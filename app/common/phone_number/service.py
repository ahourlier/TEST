from typing import Dict, List

from flask_sqlalchemy import Model

from app import db
from app.common.phone_number.model import PhoneNumber


class PhoneNumberService:
    @staticmethod
    def update_phone_numbers(entity: Model, updated_phones: List[Dict], commit=False):
        existing_phones_dict = dict()
        for existing_phone in entity.phones:
            existing_phones_dict[existing_phone.id] = existing_phone

        for phone in updated_phones:
            if "id" in phone:
                existing_phone = existing_phones_dict[phone.get("id")]
                if PhoneNumberService.has_changed(existing_phone, phone):
                    for k, v in phone.items():
                        setattr(existing_phone, k, v)
                del existing_phones_dict[phone.get("id")]
            else:
                phone["resource_id"] = entity.id
                phone["resource_type"] = entity.__class__.__name__.lower()
                db.session.add(PhoneNumber(**phone))
        for to_remove in existing_phones_dict.values():
            db.session.delete(to_remove)

        if commit:
            db.session.commit()

    @staticmethod
    def has_changed(old_phone: PhoneNumber, changes: Dict) -> bool:
        return (
            old_phone.country_code != changes.get("country_code")
            or old_phone.national != changes.get("national")
            or old_phone.international != changes.get("international")
        )

    @staticmethod
    def get_by_id(phone_id: str) -> PhoneNumber:
        db_phone_number = PhoneNumber.query.get(phone_id)
        return db_phone_number

    @staticmethod
    def delete_by_id(phone_number_id: int) -> int or None:
        phone_number = PhoneNumber.query.filter(
            PhoneNumber.id == phone_number_id
        ).first()
        db.session.delete(phone_number)
        db.session.commit()
        return phone_number_id
