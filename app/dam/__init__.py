BASE_ROUTE = "dam"


def register_routes(api, app, root="api"):
    from .documents.controller import api as documents_api

    api.add_namespace(documents_api, path=f"/{root}/{BASE_ROUTE}/documents")


def register_internal_routes(bp):
    from .documents.internal_controller import DocsGenerationView, DocsEditView

    prefix = "/documents"
    bp.add_url_rule(
        f"{prefix}/generate",
        view_func=DocsGenerationView.as_view("document-generate"),
        methods=["POST"],
    )
    bp.add_url_rule(
        f"{prefix}/edit",
        view_func=DocsEditView.as_view("document-edit"),
        methods=["POST"],
    )


def register_routes_v2(api, app, root="api"):
    from .documents_v2.controller import api as documents_v2_api

    api.add_namespace(documents_v2_api, path=f"/{root}/{BASE_ROUTE}/documentsV2")


def register_internal_routes_v2(bp):
    from .documents_v2.internal_controller import DocsGenerationViewV2, DocsEditViewV2

    prefix = "/documents"
    bp.add_url_rule(
        f"{prefix}/generate",
        view_func=DocsGenerationViewV2.as_view("document-generate"),
        methods=["POST"],
    )
    bp.add_url_rule(
        f"{prefix}/edit",
        view_func=DocsEditViewV2.as_view("document-edit"),
        methods=["POST"],
    )
