from typing import List

import app.project.requesters.service as requester_service
from app import db
from app.common.exceptions import InconsistentUpdateIdException
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.project.contacts import Contact
from app.project.contacts.error_handlers import ContactNotFoundException
from app.project.contacts.interface import ContactInterface
import app.common.phone_number.service as phone_numbers_service


class ContactService:
    @staticmethod
    def create(new_attrs: ContactInterface, commit: bool = True) -> Contact:
        """Create a new contact with linked requester"""
        requester_service.RequesterService.get_by_id(new_attrs.get("requester_id"))
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]
        contact = Contact(**new_attrs)
        db.session.add(contact)
        if commit:
            db.session.commit()
        return contact

    @staticmethod
    def create_list(
        new_contacts: List[ContactInterface], requester_id: int
    ) -> List[Contact]:
        """Create contacts from a list"""
        contacts = []
        for contact in new_contacts:
            contact["requester_id"] = requester_id
            contacts.append(ContactService.create(contact))
        return contacts

    @staticmethod
    def get_by_id(contact_id: str) -> Contact:
        db_contact = Contact.query.get(contact_id)
        if db_contact is None:
            raise ContactNotFoundException
        return db_contact

    @staticmethod
    def update(
        contact: Contact, changes: ContactInterface, force_update: bool = False
    ) -> Contact:
        if force_update or ContactService.has_changed(contact, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != contact.id:
                raise InconsistentUpdateIdException()
            if "phone_number" in changes:
                if changes.get("phone_number", None):
                    PhoneNumberService.update_phone_numbers(
                        contact, [changes.get("phone_number")]
                    )
                del changes["phone_number"]
            contact.update(changes)
            db.session.commit()
        return contact

    @staticmethod
    def update_list(list_changes, requester_id: int):

        old_contacts = Contact.query.filter_by(requester_id=requester_id).all()

        for contact_changes in list_changes:
            # If contact exists, it must be updated
            if "id" in contact_changes:
                contact = ContactService.get_by_id(contact_changes["id"])
                ContactService.update(contact, contact_changes)
            # Else, it must be created
            else:
                contact_changes["requester_id"] = requester_id
                ContactService.create(contact_changes, False)

        # Compare old contact list and new list and delete obsolete contacts
        for old_contact in old_contacts:
            is_removed = True
            for new_contact in list_changes:
                if "id" in new_contact and new_contact["id"] == old_contact.id:
                    is_removed = False
                    break
            if is_removed:
                ContactService.delete_by_id(old_contact.id)

    @staticmethod
    def has_changed(contact: Contact, changes: ContactInterface) -> bool:
        for key, value in changes.items():
            if getattr(contact, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(contact_id: int) -> int or None:
        contact = Contact.query.filter(Contact.id == contact_id).first()
        if contact.phone_number:
            phone_numbers_service.PhoneNumberService.delete_by_id(
                contact.phone_number.id
            )
        if not contact:
            raise ContactNotFoundException
        db.session.delete(contact)
        db.session.commit()
        return contact_id
