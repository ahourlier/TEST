import imp
from app import db
from app.common.app_name import App
from app.mission.missions import Mission
from app.thematique.model import ThematiqueMission
from app.thematique.service import ThematiqueService


def init_missions_thematiques():
    missions = (
        Mission.query.join(ThematiqueMission, isouter=True)
        .filter(Mission.mission_type == App.COPRO)
        .all()
    )
    for m in missions:
        ThematiqueService.init_mission_thematics(m.id)
