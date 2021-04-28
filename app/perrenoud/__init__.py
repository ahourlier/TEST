BASE_ROUTE = "perrenoud"
from .scenarios.model import Scenario
from .heatings.model import Heating
from .hot_waters.model import HotWater
from .walls.model import Wall
from .recommendations.model import Recommendation
from .woodworks.model import Woodwork
from .ceilings.model import Ceiling
from .floors.model import Floor
from .thermal_bridges.model import ThermalBridge
from .rooms.model import Room
from .room_inputs.model import RoomInput
from .areas.model import Area

from .scenarios.controller import api as scenarios_api
from .heatings.controller import api as heatings_api
from .walls.controller import api as walls_api
from .woodworks.controller import api as woodworks_api
from .ceilings.controller import api as ceilings_api
from .floors.controller import api as floors_api
from .thermal_bridges.controller import api as thermal_bridges_api
from .rooms.controller import api as rooms_api
from .photos.controller import api as photo_api
from .recommendations.controller import api as recommendations_api


def register_routes(api, app, root="api"):
    api.add_namespace(scenarios_api, path=f"/{root}/{BASE_ROUTE}/scenarios")
    api.add_namespace(photo_api, path=f"/{root}/{BASE_ROUTE}/photos")
    api.add_namespace(recommendations_api, path=f"/{root}/{BASE_ROUTE}/recommendations")
    api.add_namespace(heatings_api, path=f"/{root}/{BASE_ROUTE}/heatings")
    api.add_namespace(rooms_api, path=f"/{root}/{BASE_ROUTE}/rooms")
    api.add_namespace(ceilings_api, path=f"/{root}/{BASE_ROUTE}/ceilings")
    api.add_namespace(walls_api, path=f"/{root}/{BASE_ROUTE}/walls")
    api.add_namespace(woodworks_api, path=f"/{root}/{BASE_ROUTE}/woodworks")
    api.add_namespace(floors_api, path=f"/{root}/{BASE_ROUTE}/floors")
    api.add_namespace(thermal_bridges_api, path=f"/{root}/{BASE_ROUTE}/bridges")


def register_internal_routes(bp):
    from .photos.internal_controller import RenamePhotoRoomView, RenamePhotosRoomView

    prefix = "/rename_photos"
    bp.add_url_rule(
        f"{prefix}/multiple",
        view_func=RenamePhotosRoomView.as_view("rename-photos-room"),
        methods=["POST"],
    )
    bp.add_url_rule(
        f"{prefix}/single",
        view_func=RenamePhotoRoomView.as_view("rename-photo-room-files"),
        methods=["POST"],
    )
