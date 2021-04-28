from app.common.error_handlers import parse_exception
from app.project.project_leads import api
from app.project.project_leads.exceptions import (
    ProjectLeadNotFoundException,
    UnidentifiedReferrerException,
)


@api.errorhandler(ProjectLeadNotFoundException)
def project_lead_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(UnidentifiedReferrerException)
def unidentified_referrer(error):  # pragma: no cover
    return parse_exception(error)
