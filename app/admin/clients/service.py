from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from .error_handlers import ClientNotFoundException
from .exceptions import ChildClientMissionException
from .interface import ClientInterface
from .model import Client
from app.admin.error_handlers import InconsistentUpdateIdException
from ...common.exceptions import ChildMissionException
from ...common.phone_number.model import PhoneNumber
from ...common.phone_number.service import PhoneNumberService
from ...common.search import sort_query

from app import db

CLIENTS_DEFAULT_PAGE = 1
CLIENTS_DEFAULT_PAGE_SIZE = 100
CLIENTS_DEFAULT_SORT_FIELD = "id"
CLIENTS_DEFAULT_SORT_DIRECTION = "desc"


class ClientService:
    @staticmethod
    def get_all(
        page=CLIENTS_DEFAULT_PAGE,
        size=CLIENTS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=CLIENTS_DEFAULT_SORT_FIELD,
        direction=CLIENTS_DEFAULT_SORT_DIRECTION,
    ) -> Pagination:
        q = sort_query(Client.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Client.name.ilike(search_term),
                    Client.postal_address.ilike(search_term),
                    Client.last_name.ilike(search_term),
                    Client.first_name.ilike(search_term),
                )
            )

        # Deactivated clients must not be retrieved
        q = q.filter(Client.active == True)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(client_id: int) -> Client:
        db_client = Client.query.get(client_id)
        if db_client is None or not db_client.active:
            raise ClientNotFoundException
        return db_client

    @staticmethod
    def create(new_attrs: ClientInterface) -> Client:
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]
        new_client = Client(**new_attrs)
        db.session.add(new_client)
        db.session.commit()
        return new_client

    @staticmethod
    def update(
        client: Client, changes: ClientInterface, force_update: bool = False
    ) -> Client:
        if force_update or ClientService.has_changed(client, changes):
            if changes.get("id") and changes.get("id") != client.id:
                raise InconsistentUpdateIdException
            if "phone_number" in changes:
                if changes.get("phone_number", None):
                    PhoneNumberService.update_phone_numbers(
                        client, [changes.get("phone_number")]
                    )
                del changes["phone_number"]
            client.update(changes)
            db.session.commit()
        return client

    @staticmethod
    def has_changed(client: Client, changes: ClientInterface) -> bool:
        for key, value in changes.items():
            if getattr(client, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(client_id: int) -> int or None:
        client = Client.query.filter(Client.id == client_id).first()
        if not client:
            raise ClientNotFoundException
        if client.missions:
            # A mission depends of this client. Must not be deleted.
            raise ChildClientMissionException
        client.active = False
        db.session.commit()
        return client_id
