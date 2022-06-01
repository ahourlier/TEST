from sqlalchemy import or_
from app import db
from app.combined_structure.model import CombinedStructure
from app.copro.copros.model import Copro
from app.building.model import Building
from app.lot.model import Lot


class DBUtils:
    def soft_delete_cascade(entity_id, service):
        """Soft delete an entity and all its children"""
        from app.task.service import TaskService

        existing_entity = service.get(entity_id)
        if type(existing_entity) == CombinedStructure:
            # First delete all associated tasks
            tasks = TaskService.get_by_entity(str(existing_entity.id), "sc_id")
            for task in tasks:
                task.soft_delete()
            # Soft delete all copros
            copros = (
                Copro.query.with_entities(Copro.id)
                .filter(Copro.cs_id == entity_id)
                .filter(or_(Copro.is_deleted == False, Copro.is_deleted == None))
                .all()
            )
            for copro in copros:
                from app.copro.copros.service import CoproService
                DBUtils.soft_delete_cascade(copro.id, CoproService)

        if type(existing_entity) == Copro:
            # First delete all associated tasks
            tasks = TaskService.get_by_entity(str(existing_entity.id), "copro_id")
            for task in tasks:
                task.soft_delete()
            # Soft delete all buildings
            buildings = (
                Building.query.with_entities(Building.id)
                .filter(Building.copro_id == entity_id)
                .filter(or_(Building.is_deleted == False, Building.is_deleted == None))
                .all()
            )
            for building in buildings:
                from app.building.service import BuildingService
                DBUtils.soft_delete_cascade(building.id, BuildingService)

        if type(existing_entity) == Building:
            # First delete all associated tasks
            tasks = TaskService.get_by_entity(str(existing_entity.id), "building_id")
            for task in tasks:
                task.soft_delete()
            # Soft delete all lots
            lots = lots = (
                Lot.query.with_entities(Lot.id)
                .filter(Lot.building_id == entity_id)
                .filter(or_(Lot.is_deleted == False, Lot.is_deleted == None))
                .all()
            )
            for lot in lots:
                from app.lot.service import LotService

                DBUtils.soft_delete_cascade(lot.id, LotService)

        if type(existing_entity) == Lot:
            # First delete all associated tasks
            tasks = TaskService.get_by_entity(str(existing_entity.id), "lot_id")
            for task in tasks:
                task.soft_delete()
            existing_entity.soft_delete()
            db.session.commit()

        existing_entity.soft_delete()
        db.session.commit()
