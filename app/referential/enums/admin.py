from app.project.quotes.model import Quote
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func
from wtforms import StringField, BooleanField

from .model import AppEnum
from ... import db
from ...funder.funders import Funder
from ...mission.missions import Mission
from ...mission.missions.mission_details.job import Job
from ...mission.missions.mission_details.model import MissionDetail
from ...mission.missions.mission_details.operational_plan import OperationalPlan
from ...mission.missions.mission_details.subjob import Subjob
from ...project.accommodations import Accommodation
from ...project.disorders import DisorderType
from ...project.projects import Project
from ...project.requesters import Requester


class BaseReadOnly:
    TYPE = "readonly"

    @staticmethod
    def readonly_condition():
        return False

    def __call__(self, *args, **kwargs):
        if self.readonly_condition():
            kwargs.setdefault(self.TYPE, True)
        return super(BaseReadOnly, self).__call__(*args, **kwargs)

    def populate_obj(self, obj, name):
        if not self.readonly_condition():
            super(BaseReadOnly, self).populate_obj(obj, name)


class PrivateReadonlyStringField(BaseReadOnly, StringField):
    pass


class PrivateReadonlyBooleanField(BaseReadOnly, BooleanField):
    TYPE = "disabled"


class EnumBaseAdminView(ModelView):
    action_disallowed_list = ["delete"]
    column_list = ("name", "display_order", "disabled")
    column_labels = dict(
        name="Nom", display_order="Ordre d'affichage", disabled="Désactivé"
    )
    column_default_sort = "display_order"
    column_filters = ("disabled",)
    column_searchable_list = ("name",)
    form_columns = ("name", "display_order", "disabled")
    form_overrides = dict(
        name=PrivateReadonlyStringField, disabled=PrivateReadonlyBooleanField
    )
    list_template = "enum_list.html"

    def on_model_change(self, form, model, is_created):
        model.kind = self.ENUM_KIND

    def get_query(self):
        return (
            super(EnumBaseAdminView, self)
            .get_query()
            .filter(AppEnum.kind == self.ENUM_KIND)
        )

    def get_count_query(self):
        return (
            self.session.query(func.count("*"))
            .select_from(AppEnum)
            .filter(AppEnum.kind == self.ENUM_KIND)
        )

    def delete_model(self, model):
        if model.private:
            return False
        exists = None
        if self.FIELD_MODEL and self.FIELD_REF:
            exists = (
                self.session.query(self.FIELD_MODEL)
                .filter(getattr(self.FIELD_MODEL, self.FIELD_REF) == model.name)
                .first()
            )
        if exists is not None:
            model.disabled = True
            self.session.commit()
            return True
        return super(EnumBaseAdminView, self).delete_model(model)

    def update_model(self, form, model):
        if self.FIELD_MODEL and self.FIELD_REF:
            if form.name.data != model.name:
                attr_to_update = getattr(self.FIELD_MODEL, self.FIELD_REF)
                self.session.query(self.FIELD_MODEL).filter(
                    attr_to_update == model.name
                ).update({attr_to_update: form.name.data})

        return super(EnumBaseAdminView, self).update_model(form, model)

    def edit_form(self, obj=None):
        def readonly_condition():
            if obj is None:
                return False
            return obj.private

        form = super(EnumBaseAdminView, self).edit_form(obj)
        form.name.readonly_condition = readonly_condition
        form.disabled.readonly_condition = readonly_condition
        return form


class MissionStatusAdminView(EnumBaseAdminView):
    ENUM_KIND = "MissionStatus"
    FIELD_MODEL = Mission
    FIELD_REF = "status"


class ProjectStatusAdminView(EnumBaseAdminView):
    ENUM_KIND = "ProjectStatus"
    FIELD_MODEL = Project
    FIELD_REF = "status"


class ProjectContactSource(EnumBaseAdminView):
    ENUM_KIND = "ProjectContactSource"
    FIELD_MODEL = Requester
    FIELD_REF = "contact_source"


class ProjectRequesterType(EnumBaseAdminView):
    ENUM_KIND = "ProjectRequesterType"
    FIELD_MODEL = Requester
    FIELD_REF = "type"


class ProjectCaseType(EnumBaseAdminView):
    ENUM_KIND = "ProjectCaseType"
    FIELD_MODEL = Project
    FIELD_REF = "type"


class ProjectIneligibilityCause(EnumBaseAdminView):
    ENUM_KIND = "ProjectIneligibilityCause"
    FIELD_MODEL = Requester
    FIELD_REF = "ineligibility"


class ProjectWorksType(EnumBaseAdminView):
    ENUM_KIND = "ProjectWorksType"
    FIELD_MODEL = Project
    FIELD_REF = "work_type"


class ProjectClosureMotiveType(EnumBaseAdminView):
    ENUM_KIND = "ProjectClosureMotiveType"
    FIELD_MODEL = Project
    FIELD_REF = "closure_motive"


class ProjectAccommodationType(EnumBaseAdminView):
    ENUM_KIND = "ProjectAccommodationType"
    FIELD_MODEL = Accommodation
    FIELD_REF = "accommodation_type"


class ProjectRequesterResourceCategory(EnumBaseAdminView):
    ENUM_KIND = "ProjectRequesterResourceCategory"
    FIELD_MODEL = Requester
    FIELD_REF = "resources_category"


class ProjectRequesterProfessionType(EnumBaseAdminView):
    ENUM_KIND = "ProjectRequesterProfessionType"
    FIELD_MODEL = Requester
    FIELD_REF = "profession"


class FunderType(EnumBaseAdminView):
    ENUM_KIND = "FunderType"
    FIELD_MODEL = Funder
    FIELD_REF = "type"


class ProjectAccommodationTypology(EnumBaseAdminView):
    ENUM_KIND = "ProjectAccommodationTypology"
    FIELD_MODEL = Accommodation
    FIELD_REF = "typology"


class ProjectAccommodationAccess(EnumBaseAdminView):
    ENUM_KIND = "ProjectAccommodationAccess"
    FIELD_MODEL = Accommodation
    FIELD_REF = "access"


class ProjectAccommodationRentTypeAfterRenovation(EnumBaseAdminView):
    ENUM_KIND = "ProjectAccommodationRentTypeAfterRenovation"
    FIELD_MODEL = Accommodation
    FIELD_REF = "type_rent_after_renovation"


class ProjectHeatingAnalysis(EnumBaseAdminView):
    ENUM_KIND = "ProjectHeatingAnalysis"
    FIELD_MODEL = DisorderType
    FIELD_REF = "type_name"


class ProjectAdaptationAnalysis(EnumBaseAdminView):
    ENUM_KIND = "ProjectAdaptationAnalysis"
    FIELD_MODEL = DisorderType
    FIELD_REF = "type_name"


class ProjectTechnicalAnalysis(EnumBaseAdminView):
    ENUM_KIND = "ProjectTechnicalAnalysis"
    FIELD_MODEL = DisorderType
    FIELD_REF = "type_name"


class ProjectHeatingRecommendation(EnumBaseAdminView):
    ENUM_KIND = "ProjectHeatingRecommendation"
    FIELD_MODEL = DisorderType
    FIELD_REF = "type_name"


class ProjectAdaptationRecommendation(EnumBaseAdminView):
    ENUM_KIND = "ProjectAdaptationRecommendation"
    FIELD_MODEL = DisorderType
    FIELD_REF = "type_name"


class ProjectTechnicalRecommendation(EnumBaseAdminView):
    ENUM_KIND = "ProjectTechnicalRecommendation"
    FIELD_MODEL = DisorderType
    FIELD_REF = "type_name"


class QuoteCompanyOrigin(EnumBaseAdminView):
    ENUM_KIND = "QuoteCompanyOrigin"
    FIELD_MODEL = Quote
    FIELD_REF = "company_origin"


class MissionOperationalPlan(EnumBaseAdminView):
    ENUM_KIND = "OperationalPlan"
    FIELD_MODEL = MissionDetail
    FIELD_REF = "operational_plan"


class MissionJob(EnumBaseAdminView):
    ENUM_KIND = "Job"
    FIELD_MODEL = MissionDetail
    FIELD_REF = "job"


class MissionSubjob(EnumBaseAdminView):
    ENUM_KIND = "Subjob"
    FIELD_MODEL = MissionDetail
    FIELD_REF = "subjob"
