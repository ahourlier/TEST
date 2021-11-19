from app.referential.enums import AppEnum
from app.referential.enums.admin import (
    ProjectStatusAdminView,
    MissionStatusAdminView,
    ProjectContactSource,
    ProjectRequesterType,
    ProjectRequesterResourceCategory,
    ProjectRequesterProfessionType,
    ProjectCaseType,
    ProjectIneligibilityCause,
    ProjectWorksType,
    ProjectClosureMotiveType,
    ProjectAccommodationType,
    FunderType,
    ProjectAccommodationTypology,
    ProjectAccommodationRentTypeAfterRenovation,
    ProjectAccommodationAccess,
    ProjectHeatingAnalysis,
    ProjectAdaptationAnalysis,
    ProjectTechnicalAnalysis,
    ProjectHeatingRecommendation,
    ProjectAdaptationRecommendation,
    ProjectTechnicalRecommendation,
    QuoteCompanyOrigin,
    MissionOperationalPlan,
    MissionJob,
    MissionSubjob,
    CoproConstructionTime,
    CoproType,
    SyndicType,
)


def register_admin_views(admin, db):
    admin.add_view(
        MissionStatusAdminView(
            AppEnum,
            db.session,
            "Statut Mission",
            url="statut-mission",
            endpoint="manage_mission_status",
        )
    )
    admin.add_view(
        ProjectStatusAdminView(
            AppEnum,
            db.session,
            "Statut Projet",
            url="statut-projet",
            endpoint="manage_project_status",
        )
    )
    admin.add_view(
        ProjectContactSource(
            AppEnum,
            db.session,
            "Origine contact",
            url="origine-contact",
            endpoint="manage_project_contact_source",
        )
    )
    admin.add_view(
        ProjectRequesterType(
            AppEnum,
            db.session,
            "Type de demandeur",
            url="type-de-demandeur",
            endpoint="manage_project_requester_type",
        )
    ),
    admin.add_view(
        ProjectRequesterResourceCategory(
            AppEnum,
            db.session,
            "Catégories de ressources",
            url="categories-de-ressources",
            endpoint="manage_project_categories_resource",
        )
    ),
    admin.add_view(
        ProjectRequesterProfessionType(
            AppEnum,
            db.session,
            "Situation professionnelle",
            url="situation-professionnelle",
            endpoint="manage_project_situation_professionnelle",
        )
    )
    admin.add_view(
        ProjectCaseType(
            AppEnum,
            db.session,
            "Type de dossier",
            url="type-de-dossier",
            endpoint="manage_project_case_type",
        )
    )
    admin.add_view(
        ProjectIneligibilityCause(
            AppEnum,
            db.session,
            "Cause inéligibilité",
            url="cause-ineligibilite",
            endpoint="manage_prject_ineligibility_cause",
        ),
    )
    admin.add_view(
        ProjectWorksType(
            AppEnum,
            db.session,
            "Type de travaux",
            url="type-de-travaux",
            endpoint="manage_project_works_type",
        )
    )
    admin.add_view(
        ProjectClosureMotiveType(
            AppEnum,
            db.session,
            "Raison projet sans suite",
            url="raison-projet-sans-suite",
            endpoint="manage_project_closure_motive_type",
        )
    )
    admin.add_view(
        ProjectAccommodationType(
            AppEnum,
            db.session,
            "Type de logement",
            url="type-de-logement",
            endpoint="manage_project_accommodation_type",
        )
    )
    admin.add_view(
        FunderType(
            AppEnum,
            db.session,
            "Type de financeur",
            url="type-de-financeur",
            endpoint="manage_funder_type",
        )
    )
    admin.add_view(
        ProjectAccommodationTypology(
            AppEnum,
            db.session,
            "Typologie de logement",
            url="typologie-de-logement",
            endpoint="manage_accommodation_typology",
        )
    )
    admin.add_view(
        ProjectAccommodationRentTypeAfterRenovation(
            AppEnum,
            db.session,
            "Type de loyer après travaux",
            url="type-de-loyer-apres-travaux",
            endpoint="manage_accommodation_rent_type_after_renovation",
        )
    )
    admin.add_view(
        ProjectAccommodationAccess(
            AppEnum,
            db.session,
            "Accès logement",
            url="access-logement",
            endpoint="manage_accommodation_access",
        )
    )
    admin.add_view(
        ProjectHeatingAnalysis(
            AppEnum,
            db.session,
            "Constats thermiques",
            url="analysis-heating",
            endpoint="manage_heating_analysis",
        )
    )
    admin.add_view(
        ProjectAdaptationAnalysis(
            AppEnum,
            db.session,
            "Constats adaptation",
            url="analysis-adaptation",
            endpoint="manage_adaptation_analysis",
        )
    )
    admin.add_view(
        ProjectTechnicalAnalysis(
            AppEnum,
            db.session,
            "Constats techniques",
            url="analysis-technical",
            endpoint="manage_technical_analysis",
        )
    )
    admin.add_view(
        ProjectHeatingRecommendation(
            AppEnum,
            db.session,
            "Recommandation thermiques",
            url="recommendation-heating",
            endpoint="manage_heating_recommendation",
        )
    )
    admin.add_view(
        ProjectAdaptationRecommendation(
            AppEnum,
            db.session,
            "Recommandation adaptation",
            url="recommendation-adaptation",
            endpoint="manage_adaptation_recommendation",
        )
    )
    admin.add_view(
        ProjectTechnicalRecommendation(
            AppEnum,
            db.session,
            "Recommandation techniques",
            url="recommendation-technical",
            endpoint="manage_technical_recommendation",
        )
    )
    admin.add_view(
        QuoteCompanyOrigin(
            AppEnum,
            db.session,
            "Origine de l'entreprise",
            url="company-origin",
            endpoint="manage_company_origin",
        )
    )
    admin.add_view(
        MissionOperationalPlan(
            AppEnum,
            db.session,
            "Dispositif opérationel",
            url="operational-plan-mission",
            endpoint="manage_operational_plans",
        )
    )
    admin.add_view(
        MissionJob(
            AppEnum,
            db.session,
            "Type de métier",
            url="job-mission",
            endpoint="manage_jobs",
        )
    )
    admin.add_view(
        MissionSubjob(
            AppEnum,
            db.session,
            "Sous métier",
            url="subjob-mission",
            endpoint="manage_subjobs",
        )
    )
    admin.add_view(
        CoproConstructionTime(
            AppEnum,
            db.session,
            "Période de construction",
            url="construction-time-copro",
            endpoint="manage_construction_times",
        )
    )
    admin.add_view(
        CoproType(
            AppEnum,
            db.session,
            "Type de copropriété (mono, copro, ...)",
            url="copro-type-copro",
            endpoint="manage_copro_types",
        )
    )
    admin.add_view(
        SyndicType(
            AppEnum,
            db.session,
            "Type de syndic",
            url="synduc-type-copro",
            endpoint="manage_syndic_types",
        )
    )
