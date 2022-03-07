from sqlalchemy import or_, exc
from flask import g
from app import db
from app.cle_repartition.interface import (
    CleRepartitionInterface,
    CleRepartitionLotLinkInterface,
)
from app.cle_repartition.model import CleRepartition, LotCleRepartition
from app.common.config_error_messages import REPARTITION_KEY_LINKED_EXCEPTION
from app.copro.copros.error_handlers import RepartitionKeyLinkedException
from app.lot import Lot
from app.lot.error_handlers import LotNotFoundException, IncorrectKeyException


class CleRepartitionService:
    @staticmethod
    def create(new_attrs: CleRepartitionInterface):
        db_cle = CleRepartition(**new_attrs)
        db.session.add(db_cle)
        db.session.commit()
        return db_cle

    @staticmethod
    def update(db_cle, changes: CleRepartitionInterface):
        db_cle.update(changes)
        db.session.commit()
        return db_cle

    @staticmethod
    def link(link_data: CleRepartitionLotLinkInterface):
        db_link = LotCleRepartition(**link_data)
        db.session.add(db_link)
        db.session.commit()
        return db_link

    @staticmethod
    def handle_links(lot_id, links):
        created = []
        existing = LotCleRepartition.query.filter(
            LotCleRepartition.lot_id == lot_id
        ).all()
        if len(existing):
            for e in existing:
                db.session.delete(e)
            db.session.commit()
        for link in links:
            is_valid = CleRepartitionService.check_if_link_valid(link, lot_id)
            if not is_valid:
                raise IncorrectKeyException
            link["lot_id"] = lot_id
            created.append(CleRepartitionService.link(link))
        return created

    @staticmethod
    def check_if_link_valid(link, lot_id):
        db_key = CleRepartition.query.get(link.get("cle_repartition_id"))
        if not db_key:
            return False
        lot = Lot.query.get(lot_id)
        if not lot:
            raise LotNotFoundException
        return db_key.copro_id == lot.copro_id

    @staticmethod
    def handle_keys(copro_id, cles_repartition):
        # fetching existing keys for this copro
        existing = CleRepartition.query.filter(
            CleRepartition.copro_id == copro_id
        ).all()

        for cle in cles_repartition:
            # if payload key has an id, it's an update
            if "id" in cle and cle.get("id"):
                for idx, e in enumerate(existing):
                    if e.id == cle.get("id"):
                        CleRepartitionService.update(e, cle)
                        # removing from existing list to keep only what is processable
                        del existing[idx]
            else:
                # if not, need to create
                cle["copro_id"] = copro_id
                CleRepartitionService.create(cle)
        # delete all keys that were not in payload
        for e in existing:
            try:
                db.session.delete(e)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                message = REPARTITION_KEY_LINKED_EXCEPTION.format(e.label)
                raise RepartitionKeyLinkedException(message)
        return None
