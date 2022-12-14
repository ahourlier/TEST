from app.project.quotes.model import Quote
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func
from wtforms import StringField, BooleanField

from .model import AppEnum
from ... import db
from ...building import Building
from ...copro.copros.model import Copro
from ...copro.syndic.model import Syndic
from ...funder.funders import Funder
from ...lot import Lot
from ...mission.missions import Mission
from ...mission.missions.mission_details.job import Job
from ...mission.missions.mission_details.model import MissionDetail
from ...mission.missions.mission_details.operational_plan import OperationalPlan
from ...mission.missions.mission_details.subjob import Subjob
from ...person import Person
from ...project.accommodations import Accommodation
from ...project.disorders import DisorderType
from ...project.projects import Project
from ...project.requesters import Requester
from ...task import Task
from ...combined_structure import CombinedStructure


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
        return AppEnum.query.filter(AppEnum.kind == self.ENUM_KIND)
        # return (
        #     super(EnumBaseAdminView, self)
        #     .get_query()
        #     .filter(AppEnum.kind == self.ENUM_KIND)
        # )

    def get_count_query(self):
        return self.session.query(func.count(AppEnum.name)).filter(
            AppEnum.kind == self.ENUM_KIND
        )
        # return (
        #     self.session.query(func.count(AppEnum.id))
        #     .select_from(AppEnum)
        #     .filter(AppEnum.kind == self.ENUM_KIND)
        # )

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


class CoproConstructionTime(EnumBaseAdminView):
    ENUM_KIND = "CoproConstructionTime"
    FIELD_MODEL = Copro
    FIELD_REF = "construction_time"


class CoproType(EnumBaseAdminView):
    ENUM_KIND = "CoproType"
    FIELD_MODEL = Copro
    FIELD_REF = "copro_type"


class SyndicType(EnumBaseAdminView):
    ENUM_KIND = "SyndicType"
    FIELD_MODEL = Syndic
    FIELD_REF = "type"


class BuildingConstructionTime(EnumBaseAdminView):
    ENUM_KIND = "BuildingConstructionTime"
    FIELD_MODEL = Building
    FIELD_REF = "construction_time"


class BuildingERPCategory(EnumBaseAdminView):
    ENUM_KIND = "BuildingERPCategory"
    FIELD_MODEL = Building
    FIELD_REF = "erp_category"


class BuildingAccessType(EnumBaseAdminView):
    ENUM_KIND = "AccessType"
    FIELD_MODEL = Building
    FIELD_REF = "access_type"


class BuildingCollectiveHeater(EnumBaseAdminView):
    ENUM_KIND = "CollectiveHeater"
    FIELD_MODEL = Building
    FIELD_REF = "collective_heater"


class BuildingAsbestosDiagnosisResult(EnumBaseAdminView):
    ENUM_KIND = "AsbestosDiagnosisResult"
    FIELD_MODEL = Building
    FIELD_REF = "asbestos_diagnosis_result"


class LotType(EnumBaseAdminView):
    ENUM_KIND = "LotType"
    FIELD_MODEL = Lot
    FIELD_REF = "type"


class LotHabitationType(EnumBaseAdminView):
    ENUM_KIND = "LotHabitationType"
    FIELD_MODEL = Lot
    FIELD_REF = "habitation_type"


class LotOccupantStatus(EnumBaseAdminView):
    ENUM_KIND = "LotOccupantStatus"
    FIELD_MODEL = Lot
    FIELD_REF = "occupant_status"


class LotLeaseType(EnumBaseAdminView):
    ENUM_KIND = "LotLeaseType"
    FIELD_MODEL = Lot
    FIELD_REF = "lease_type"


class LotConventionRentType(EnumBaseAdminView):
    ENUM_KIND = "LotConventionRentType"
    FIELD_MODEL = Lot
    FIELD_REF = "convention_rent_type"


class PersonStatus(EnumBaseAdminView):
    ENUM_KIND = "PersonStatus"
    FIELD_MODEL = Person
    FIELD_REF = "status"


class TaskStatus(EnumBaseAdminView):
    ENUM_KIND = "TaskStatus"
    FIELD_MODEL = Task
    FIELD_REF = "status"


class TypePretCollectif(EnumBaseAdminView):
    ENUM_KIND = "TypePretCollectif"
    FIELD_MODEL = None
    FIELD_REF = None


class NatureTravauxInteretCollectifsPP(EnumBaseAdminView):
    ENUM_KIND = "NatureTravauxInteretCollectifsPP"
    FIELD_MODEL = None
    FIELD_REF = None


class TypePretIndividuel(EnumBaseAdminView):
    ENUM_KIND = "TypePretIndividuel"
    FIELD_MODEL = None
    FIELD_REF = None


class PreFunderOrganism(EnumBaseAdminView):
    ENUM_KIND = "PreFunderOrganism"
    FIELD_MODEL = None
    FIELD_REF = None


class NatureTravauxPartieCommune(EnumBaseAdminView):
    ENUM_KIND = "NatureTravauxPartieCommune"
    FIELD_MODEL = None
    FIELD_REF = None


class CombinedStructureType(EnumBaseAdminView):
    ENUM_KIND = "CombinedStructureType"
    FIELD_MODEL = CombinedStructure
    FIELD_REF = "type"


class MainOccupantAge(EnumBaseAdminView):
    ENUM_KIND = "MainOccupantAge"
    FIELD_MODEL = None
    FIELD_REF = None


class HouseholdDebtRate(EnumBaseAdminView):
    ENUM_KIND = "HouseholdDebtRate"
    FIELD_MODEL = None
    FIELD_REF = None


class LotSeniorityOccupation(EnumBaseAdminView):
    ENUM_KIND = "LotSeniorityOccupation"
    FIELD_MODEL = None
    FIELD_REF = None


class RentLevel(EnumBaseAdminView):
    ENUM_KIND = "RentLevel"
    FIELD_MODEL = None
    FIELD_REF = None


class HouseholdResourcesAnahStatus(EnumBaseAdminView):
    ENUM_KIND = "HouseholdResourcesAnahStatus"
    FIELD_MODEL = None
    FIELD_REF = None


class HouseholdOtherFunderLimitStatus(EnumBaseAdminView):
    ENUM_KIND = "HouseholdOtherFunderLimitStatus"
    FIELD_MODEL = None
    FIELD_REF = None


class LocatairesRessources(EnumBaseAdminView):
    ENUM_KIND = "LocatairesRessources"
    FIELD_MODEL = None
    FIELD_REF = None


class HouseholdEnergeticEffortRate(EnumBaseAdminView):
    ENUM_KIND = "HouseholdEnergeticEffortRate"
    FIELD_MODEL = None
    FIELD_REF = None


class EnergeticPrecariousnessCause(EnumBaseAdminView):
    ENUM_KIND = "EnergeticPrecariousnessCause"
    FIELD_MODEL = None
    FIELD_REF = None


class Overoccupation(EnumBaseAdminView):
    ENUM_KIND = "Overoccupation"
    FIELD_MODEL = None
    FIELD_REF = None


class HouseholdAccompaniedStatusAndPreviousStatus(EnumBaseAdminView):
    ENUM_KIND = "HouseholdAccompaniedStatusAndPreviousStatus"
    FIELD_MODEL = None
    FIELD_REF = None


class AdministrativeSituation(EnumBaseAdminView):
    ENUM_KIND = "AdministrativeSituation"
    FIELD_MODEL = None
    FIELD_REF = None


class MaritalSituation(EnumBaseAdminView):
    ENUM_KIND = "MaritalSituation"
    FIELD_MODEL = None
    FIELD_REF = None


class MovingHouseProject(EnumBaseAdminView):
    ENUM_KIND = "MovingHouseProject"
    FIELD_MODEL = None
    FIELD_REF = None


class MonthlyRessourcesType(EnumBaseAdminView):
    ENUM_KIND = "MonthlyRessourcesType"
    FIELD_MODEL = None
    FIELD_REF = None


class DebtOrigin(EnumBaseAdminView):
    ENUM_KIND = "DebtOrigin"
    FIELD_MODEL = None
    FIELD_REF = None


class PrincipalSocialProblematics(EnumBaseAdminView):
    ENUM_KIND = "PrincipalSocialProblematics"
    FIELD_MODEL = None
    FIELD_REF = None


class SocialSupportType(EnumBaseAdminView):
    ENUM_KIND = "SocialSupportType"
    FIELD_MODEL = None
    FIELD_REF = None


class RDVType(EnumBaseAdminView):
    ENUM_KIND = "RDVType"
    FIELD_MODEL = None
    FIELD_REF = None


class AdministrativeSupport(EnumBaseAdminView):
    ENUM_KIND = "AdministrativeSupport"
    FIELD_MODEL = None
    FIELD_REF = None


class InformativeEventsOrganization(EnumBaseAdminView):
    ENUM_KIND = "InformativeEventsOrganization"
    FIELD_MODEL = None
    FIELD_REF = None


class ProfessionalSituation(EnumBaseAdminView):
    ENUM_KIND = "ProfessionalSituation"
    FIELD_MODEL = None
    FIELD_REF = None


class ContractType(EnumBaseAdminView):
    ENUM_KIND = "ContractType"
    FIELD_MODEL = None
    FIELD_REF = None


class WorkAxis(EnumBaseAdminView):
    ENUM_KIND = "WorkAxis"
    FIELD_MODEL = None
    FIELD_REF = None


class PreLitigationAction(EnumBaseAdminView):
    ENUM_KIND = "PreLitigationAction"
    FIELD_MODEL = None
    FIELD_REF = None


class UrbanisAction(EnumBaseAdminView):
    ENUM_KIND = "UrbanisAction"
    FIELD_MODEL = None
    FIELD_REF = None


class LitigationAction(EnumBaseAdminView):
    ENUM_KIND = "LitigationAction"
    FIELD_MODEL = None
    FIELD_REF = None


class ArchitectQualification(EnumBaseAdminView):
    ENUM_KIND = "ArchitectQualification"
    FIELD_MODEL = None
    FIELD_REF = None


class SecurityCommissionResult(EnumBaseAdminView):
    ENUM_KIND = "SecurityCommissionResult"
    FIELD_MODEL = None
    FIELD_REF = None


class LocalisationCopropriete(EnumBaseAdminView):
    ENUM_KIND = "LocalisationCopropriete"
    FIELD_MODEL = None
    FIELD_REF = None


class WaterBillingType(EnumBaseAdminView):
    ENUM_KIND = "WaterBillingType"
    FIELD_MODEL = None
    FIELD_REF = None


class HeaterBillingType(EnumBaseAdminView):
    ENUM_KIND = "HeaterBillingType"
    FIELD_MODEL = None
    FIELD_REF = None


class MeetingTheme(EnumBaseAdminView):
    ENUM_KIND = "MeetingTheme"
    FIELD_MODEL = None
    FIELD_REF = None


class ActionUrbanisThemeGUP(EnumBaseAdminView):
    ENUM_KIND = "ActionUrbanisThemeGUP"
    FIELD_MODEL = None
    FIELD_REF = None


class OtherActionUrbanis(EnumBaseAdminView):
    ENUM_KIND = "OtherActionUrbanis"
    FIELD_MODEL = None
    FIELD_REF = None


class NatureDysfunction(EnumBaseAdminView):
    ENUM_KIND = "NatureDysfunction"
    FIELD_MODEL = None
    FIELD_REF = None


class ActionType(EnumBaseAdminView):
    ENUM_KIND = "ActionType"
    FIELD_MODEL = None
    FIELD_REF = None


class CommunicationActionType(EnumBaseAdminView):
    ENUM_KIND = "CommunicationActionType"
    FIELD_MODEL = None
    FIELD_REF = None


class ActionResponsibleCommunication(EnumBaseAdminView):
    ENUM_KIND = "ActionResponsibleCommunication"
    FIELD_MODEL = None
    FIELD_REF = None


class FormationType(EnumBaseAdminView):
    ENUM_KIND = "FormationType"
    FIELD_MODEL = None
    FIELD_REF = None


class Former(EnumBaseAdminView):
    ENUM_KIND = "Former"
    FIELD_MODEL = None
    FIELD_REF = None


class ActionResponsibleFormation(EnumBaseAdminView):
    ENUM_KIND = "ActionResponsibleFormation"
    FIELD_MODEL = None
    FIELD_REF = None


class AGType(EnumBaseAdminView):
    ENUM_KIND = "AGType"
    FIELD_MODEL = None
    FIELD_REF = None


class Renegociation(EnumBaseAdminView):
    ENUM_KIND = "Renegociation"
    FIELD_MODEL = None
    FIELD_REF = None


class CompetitionReopening(EnumBaseAdminView):
    ENUM_KIND = "CompetitionReopening"
    FIELD_MODEL = None
    FIELD_REF = None


class ConsumptionLabel(EnumBaseAdminView):
    ENUM_KIND = "ConsumptionLabel"
    FIELD_MODEL = None
    FIELD_REF = None


class ProcedureCommonParts(EnumBaseAdminView):
    ENUM_KIND = "ProcedureCommonParts"
    FIELD_MODEL = None
    FIELD_REF = None


class ProcedurePrivateParts(EnumBaseAdminView):
    ENUM_KIND = "ProcedurePrivateParts"
    FIELD_MODEL = None
    FIELD_REF = None


class WorkNatureAssetPlan(EnumBaseAdminView):
    ENUM_KIND = "WorkNatureAssetPlan"
    FIELD_MODEL = None
    FIELD_REF = None


class WorkEligibleSubsidiesHeritagePlan(EnumBaseAdminView):
    ENUM_KIND = "WorkEligibleSubsidiesHeritagePlan"
    FIELD_MODEL = None
    FIELD_REF = None


class ActionResponsible(EnumBaseAdminView):
    ENUM_KIND = "ActionResponsible"
    FIELD_MODEL = None
    FIELD_REF = None


class WorkNatureCommonParts(EnumBaseAdminView):
    ENUM_KIND = "WorkNatureCommonParts"
    FIELD_MODEL = None
    FIELD_REF = None


class WorkNatureCollectiveInterestPrivateParts(EnumBaseAdminView):
    ENUM_KIND = "WorkNatureCollectiveInterestPrivateParts"
    FIELD_MODEL = None
    FIELD_REF = None


class HelpType(EnumBaseAdminView):
    ENUM_KIND = "HelpType"
    FIELD_MODEL = None
    FIELD_REF = None


class IndividualLoanType(EnumBaseAdminView):
    ENUM_KIND = "IndividualLoanType"
    FIELD_MODEL = None
    FIELD_REF = None


class WorkNaturePrivateParts(EnumBaseAdminView):
    ENUM_KIND = "WorkNaturePrivateParts"
    FIELD_MODEL = None
    FIELD_REF = None


class FunderOrganism(EnumBaseAdminView):
    ENUM_KIND = "FunderOrganism"
    FIELD_MODEL = None
    FIELD_REF = None


class SupportingStructure(EnumBaseAdminView):
    ENUM_KIND = "SupportingStructure"
    FIELD_MODEL = None
    FIELD_REF = None


class BuyerSales(EnumBaseAdminView):
    ENUM_KIND = "BuyerSales"
    FIELD_MODEL = None
    FIELD_REF = None


class NatureSuivi(EnumBaseAdminView):
    ENUM_KIND = "NatureSuivi"
    FIELD_MODEL = None
    FIELD_REF = None


class FSLType(EnumBaseAdminView):
    ENUM_KIND = "FSLType"
    FIELD_MODEL = None
    FIELD_REF = None


class AccompaniementClosing(EnumBaseAdminView):
    ENUM_KIND = "AccompaniementClosing"
    FIELD_MODEL = None
    FIELD_REF = None


class FinancialDeviceType(EnumBaseAdminView):
    ENUM_KIND = "FinancialDeviceType"
    FIELD_MODEL = None
    FIELD_REF = None


class HeightClassification(EnumBaseAdminView):
    ENUM_KIND = "HeightClassification"
    FIELD_MODEL = None
    FIELD_REF = None
