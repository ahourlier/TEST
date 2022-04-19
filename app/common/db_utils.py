from app import db
from app.combined_structure.model import CombinedStructure
from app.copro.copros.model import Copro
from app.building.model import Building
from app.lot.model import Lot

class DBUtils:

    def soft_delete_cascade(entity_id, service):
        """Soft delete an entity and all its children"""
        existing_entity = service.get(entity_id)
        if type(existing_entity) == CombinedStructure:
            # Soft delete all copros
            copros = (
                Copro.query.with_entities(Copro.id)
                .filter(Copro.cs_id == entity_id)
                .all()
            )
            for copro in copros:
                from app.copro.copros.service import CoproService
                DBUtils.soft_delete_cascade(copro.id, CoproService)

        if type(existing_entity) == Copro:
            # Soft delete all buildings
            buildings = (
                Building.query.with_entities(Building.id)
                .filter(Building.copro_id == entity_id)
                .all()
            )
            for building in buildings:
                from app.building.service import BuildingService
                DBUtils.soft_delete_cascade(building.id, BuildingService)

        if type(existing_entity) == Building:
            # Soft delete all lots
            lots = lots = (
                Lot.query.with_entities(Lot.id)
                .filter(Lot.building_id == entity_id)
                .all()
            )
            for lot in lots:
                from app.lot.service import LotService
                DBUtils.soft_delete_cascade(lot.id, LotService)
                
        if type(existing_entity) == Lot:
            existing_entity.soft_delete()
            db.session.commit()

        existing_entity.soft_delete()
        db.session.commit()