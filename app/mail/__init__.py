BASE_ROUTE = "email"

from .mails.controller import api as emails_api


def register_routes(api, app, root="api"):
    api.add_namespace(emails_api, path=f"/{root}/{BASE_ROUTE}/emails")


def register_internal_routes(bp):
    from .mails.internal_controller import EmailSendView

    prefix = "/emails"
    bp.add_url_rule(
        f"{prefix}/send",
        view_func=EmailSendView.as_view("email-send"),
        methods=["POST"],
    )
