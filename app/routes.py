def register_routes(api, app, root="api"):
    from app.auth import register_routes as attach_auth
    from app.admin import register_routes as attach_admin
    from app.mission import register_routes as attach_mission
    from app.dam import register_routes as attach_upload
    from app.project import register_routes as attach_project
    from app.referential import register_routes as attach_referential
    from app.funder import register_routes as attach_funder
    from app.mail import register_routes as attach_emails
    from app.homepage import register_routes as attach_homepage
    from app.data_import import register_routes as attach_data_import
    from app.perrenoud import register_routes as attach_perrenoud
    from app.copro import register_routes as attach_copro
    from app.building import register_routes as attach_buildings
    from app.lot import register_routes as attach_lots
    from app.person import register_routes as attach_people
    from app.thematique import register_routes as attach_thematiques

    attach_auth(api, app, root)
    attach_admin(api, app, root)
    attach_mission(api, app, root)
    attach_upload(api, app, root)
    attach_project(api, app, root)
    attach_referential(api, app, root)
    attach_funder(api, app, root)
    attach_emails(api, app, root)
    attach_homepage(api, app, root)
    attach_data_import(api, app, root)
    attach_perrenoud(api, app, root)
    attach_copro(api, app, root)
    attach_buildings(api, app, root)
    attach_lots(api, app, root)
    attach_people(api, app, root)
    attach_thematiques(api, app, root)
