from .base import internal_api_blueprint


def register_internal_routes(bp):
    from app.mission import register_internal_routes as register_internal_mission_routes
    from app.project import register_internal_routes as register_internal_project_routes
    from app.email import register_internal_routes as register_internal_email_routes
    from app.dam import register_internal_routes as register_internal_docs_routes
    from app.data_import import (
        register_internal_routes as register_internal_import_routes,
    )
    from app.perrenoud import (
        register_internal_routes as register_internal_photos_routes,
    )

    register_internal_mission_routes(bp)
    register_internal_project_routes(bp)
    register_internal_email_routes(bp)
    register_internal_docs_routes(bp)
    register_internal_import_routes(bp)
    register_internal_photos_routes(bp)


__all__ = ["internal_api_blueprint"]
