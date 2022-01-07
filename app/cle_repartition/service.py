from sqlalchemy import or_
from flask import g
from app import db
from app.cle_repartition.interface import (
    CleRepartitionInterface,
    CleRepartitionLotLinkInterface,
)
from app.cle_repartition.model import CleRepartition, LotCleRepartition
from app.lot import Lot
from app.lot.exceptions import LotNotFoundException, IncorrectKeyException


class CleRepartitionService:
    @staticmethod
    def create(new_attrs: CleRepartitionInterface):
        db_cle = CleRepartition(**new_attrs)
        db.session.add(db_cle)
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
        created = []
        existing = CleRepartition.query.filter(
            CleRepartition.copro_id == copro_id
        ).all()
        if len(existing):
            for e in existing:
                db.session.delete(e)
            db.session.commit()
        for cle in cles_repartition:
            cle["copro_id"] = copro_id
            created.append(CleRepartitionService.create(cle))
        return created
