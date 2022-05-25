from app.referential.enums import AppEnum
from app.referential.enums.admin import (
    AGType,
    AccompaniementClosing,
    ActionResponsible,
    ActionResponsibleCommunication,
    ActionResponsibleFormation,
    ActionType,
    ActionUrbanisThemeGUP,
    AdministrativeSituation,
    AdministrativeSupport,
    ArchitectQualification,
    BuyerSales,
    CombinedStructureType,
    CommunicationActionType,
    CompetitionReopening,
    ConsumptionLabel,
    ContractType,
    DebtOrigin,
    EnergeticPrecariousnessCause,
    FSLType,
    FormationType,
    Former,
    FunderOrganism,
    HeaterBillingType,
    HelpType,
    HouseholdAccompaniedStatusAndPreviousStatus,
    HouseholdDebtRate,
    HouseholdEnergeticEffortRate,
    HouseholdOtherFunderLimitStatus,
    HouseholdResourcesAnahStatus,
    IndividualLoanType,
    InformativeEventsOrganization,
    LitigationAction,
    LocalisationCopropriete,
    LocatairesRessources,
    LotSeniorityOccupation,
    MainOccupantAge,
    MaritalSituation,
    MeetingTheme,
    MovingHouseProject,
    NatureDysfunction,
    NatureSuivi,
    OtherActionUrbanis,
    Overoccupation,
    PreLitigationAction,
    ProcedureCommonParts,
    ProcedurePrivateParts,
    ProfessionalSituation,
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
    CoproConstructionTime,
    CoproType,
    RDVType,
    Renegociation,
    RentLevel,
    PrincipalSocialProblematics,
    SecurityCommissionResult,
    SocialSupportType,
    SupportingStructure,
    SyndicType,
    BuildingConstructionTime,
    BuildingERPCategory,
    BuildingAccessType,
    BuildingCollectiveHeater,
    BuildingAsbestosDiagnosisResult,
    LotType,
    LotHabitationType,
    LotOccupantStatus,
    LotLeaseType,
    LotConventionRentType,
    PersonStatus,
    TaskStatus,
    TypePretCollectif,
    NatureTravauxInteretCollectifsPP,
    TypePretIndividuel,
    Prefinanceurs,
    NatureTravauxPartieCommune,
    UrbanisAction,
    MonthlyRessourcesType,
    WaterBillingType,
    WorkAxis,
    WorkEligibleSubsidiesHeritagePlan,
    WorkNatureAssetPlan,
    WorkNatureCollectivInterestPrivateParts,
    WorkNatureCommonParts,
    WorkNaturePrivateParts,
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
    admin.add_view(
        BuildingConstructionTime(
            AppEnum,
            db.session,
            "Période de construction (bâtiment)",
            url="construction-time-building",
            endpoint="manage_construction_times_buildings",
        )
    )
    admin.add_view(
        BuildingERPCategory(
            AppEnum,
            db.session,
            "Catégorie d'ERP",
            url="erp-category-building",
            endpoint="manage_erp_categories",
        )
    )
    admin.add_view(
        BuildingAccessType(
            AppEnum,
            db.session,
            "Modalités d'accès au batiment",
            url="access-type-building",
            endpoint="manage_access_types",
        )
    )
    admin.add_view(
        BuildingCollectiveHeater(
            AppEnum,
            db.session,
            "Chauffage collectif",
            url="collective-heater-building",
            endpoint="manage_collective_heaters",
        )
    )
    admin.add_view(
        BuildingAsbestosDiagnosisResult(
            AppEnum,
            db.session,
            "Résultat diagnostic amiante",
            url="asbestos-result-building",
            endpoint="manage_asbestos_results",
        )
    )
    admin.add_view(
        LotType(
            AppEnum,
            db.session,
            "Type de lot",
            url="type-lot",
            endpoint="manage_lot_type",
        )
    )
    admin.add_view(
        LotHabitationType(
            AppEnum,
            db.session,
            "Type de logement",
            url="habitation-type-lot",
            endpoint="manage_habitation_type",
        )
    )
    admin.add_view(
        LotOccupantStatus(
            AppEnum,
            db.session,
            "Statut de l'occupant du lot",
            url="occupant-status-lot",
            endpoint="manage_occupant_status",
        )
    )
    admin.add_view(
        LotLeaseType(
            AppEnum,
            db.session,
            "Si logement loué, nature du bail",
            url="lease-type-lot",
            endpoint="manage_lease_types",
        )
    ),
    admin.add_view(
        LotConventionRentType(
            AppEnum,
            db.session,
            "Si loyer conventionné, type de loyer conventionné",
            url="convention-rent-type-lot",
            endpoint="manage_convention_rent_types",
        )
    )
    admin.add_view(
        PersonStatus(
            AppEnum,
            db.session,
            "Statut personne physique",
            url="status-person",
            endpoint="manage_person_status",
        )
    )
    admin.add_view(
        TaskStatus(
            AppEnum,
            db.session,
            "Statut tâche",
            url="status-task",
            endpoint="manage_task_status",
        )
    )
    admin.add_view(
        TypePretCollectif(
            AppEnum,
            db.session,
            "Type de prêt collectif",
            url="collective-loan-type",
            endpoint="manage_collective_loan_type",
        )
    )
    admin.add_view(
        NatureTravauxInteretCollectifsPP(
            AppEnum,
            db.session,
            "Nature des travaux intérêt collectif parties privatives",
            url="nticpp",
            endpoint="manage_nticpp",
        )
    )
    admin.add_view(
        TypePretIndividuel(
            AppEnum,
            db.session,
            "Type de prêt individuel - travaux AG",
            url="type-pret-indiv",
            endpoint="manage_type_pret_indiv",
        )
    )
    admin.add_view(
        Prefinanceurs(
            AppEnum,
            db.session,
            "Prefinanceurs",
            url="prefinanceurs",
            endpoint="manage_prefinanceurs",
        )
    )
    admin.add_view(
        NatureTravauxPartieCommune(
            AppEnum,
            db.session,
            "Nature travaux partie commune",
            url="ntpc",
            endpoint="manage_ntpc",
        )
    )
    admin.add_view(
        CombinedStructureType(
            AppEnum,
            db.session,
            "Type de Structure Combinée",
            url="combined-structure-type",
            endpoint="manage_combined_structure_type",
        )
    )
    admin.add_view(
        MainOccupantAge(
            AppEnum,
            db.session,
            "Age de l'occupant principal",
            url="main-occupant-age",
            endpoint="manage_main_occupant_age",
        )
    )
    admin.add_view(
        HouseholdDebtRate(
            AppEnum,
            db.session,
            "Taux d'endettement des ménages",
            url="household-debt-rate",
            endpoint="manage_household_debt_rate",
        )
    )
    admin.add_view(
        LotSeniorityOccupation(
            AppEnum,
            db.session,
            "Ancienneté occupation du logement",
            url="lot-seniority-occupation",
            endpoint="manage_lot_seniority_occupation",
        )
    )
    admin.add_view(
        RentLevel(
            AppEnum,
            db.session,
            "Niveau des loyers",
            url="rent-level",
            endpoint="manage_rent_level",
        )
    )
    admin.add_view(
        HouseholdResourcesAnahStatus(
            AppEnum,
            db.session,
            "Statut du ménage ressources ANAH",
            url="household-resources-anah-status",
            endpoint="manage_household_resources_anah_status",
        )
    )
    admin.add_view(
        HouseholdOtherFunderLimitStatus(
            AppEnum,
            db.session,
            "Statut du ménage ressources autres financeurs",
            url="household-other-funder-limit-status",
            endpoint="manage_household_other_funder_limit_status",
        )
    )
    admin.add_view(
        LocatairesRessources(
            AppEnum,
            db.session,
            "Ressources locataires",
            url="locataires-ressources",
            endpoint="manage_locataires_ressources",
        )
    )
    admin.add_view(
        HouseholdEnergeticEffortRate(
            AppEnum,
            db.session,
            "Taux d'effort énergétique",
            url="household-energetic-effort-rate",
            endpoint="manage_household_energetic_effort_rate",
        )
    )
    admin.add_view(
        EnergeticPrecariousnessCause(
            AppEnum,
            db.session,
            "Taux d'effort énergétique",
            url="energetic-precariousness-cause",
            endpoint="manage_energetic_precariousness_cause",
        )
    )
    admin.add_view(
        Overoccupation(
            AppEnum,
            db.session,
            "Suroccupation",
            url="suroccupation",
            endpoint="manage_suroccupation",
        )
    )
    admin.add_view(
        HouseholdAccompaniedStatusAndPreviousStatus(
            AppEnum,
            db.session,
            "Statut du ménage accompagné + Statut antérieur",
            url="household-accompanied-status",
            endpoint="manage_household_accompanied_status",
        )
    )
    admin.add_view(
        AdministrativeSituation(
            AppEnum,
            db.session,
            "Situation administrative",
            url="administrative-situation",
            endpoint="manage_administrative_situation",
        )
    )
    admin.add_view(
        MaritalSituation(
            AppEnum,
            db.session,
            "Situation matrimoniale",
            url="marital-situation",
            endpoint="manage_marital_situation",
        )
    )
    admin.add_view(
        MovingHouseProject(
            AppEnum,
            db.session,
            "Projet de déménagement",
            url="moving-house-project",
            endpoint="manage_moving_house_project",
        )
    )
    admin.add_view(
        MonthlyRessourcesType(
            AppEnum,
            db.session,
            "Type de ressources mensuelles",
            url="monthly-ressources-type",
            endpoint="manage_monthly_ressources_type",
        )
    )
    admin.add_view(
        DebtOrigin(
            AppEnum,
            db.session,
            "Origine de la dette",
            url="debt-origin",
            endpoint="manage_debt_origin",
        )
    )
    admin.add_view(
        PrincipalSocialProblematics(
            AppEnum,
            db.session,
            "Problématique sociale",
            url="social-problematics",
            endpoint="manage_social_problematics",
        )
    )
    admin.add_view(
        SocialSupportType(
            AppEnum,
            db.session,
            "Type d'accompagnement social",
            url="social-support-type",
            endpoint="manage_social_support_type",
        )
    )
    admin.add_view(
        RDVType(
            AppEnum,
            db.session,
            "Type de rdv",
            url="rdv-type",
            endpoint="manage_rdv_type",
        )
    )
    admin.add_view(
        AdministrativeSupport(
            AppEnum,
            db.session,
            "Aide administrative",
            url="administrative-support",
            endpoint="manage_administrative_support",
        )
    )
    admin.add_view(
        InformativeEventsOrganization(
            AppEnum,
            db.session,
            "Organisation d'évenements informatifs",
            url="informativ-events-organization",
            endpoint="manage_informativ_events_organization",
        )
    )
    admin.add_view(
        ProfessionalSituation(
            AppEnum,
            db.session,
            "Situation professionnelle",
            url="situation-professionnelle",
            endpoint="manage_situation_professionnelle",
        )
    )
    admin.add_view(
        ContractType(
            AppEnum,
            db.session,
            "Type de contrat",
            url="contract-type",
            endpoint="manage_contract_type",
        )
    )
    admin.add_view(
        WorkAxis(
            AppEnum,
            db.session,
            "Axe de travail",
            url="work-axis",
            endpoint="manage_work_axis",
        )
    )
    admin.add_view(
        PreLitigationAction(
            AppEnum,
            db.session,
            "Action pré-contentieuse",
            url="pre-litigation-action",
            endpoint="manage_pre_litigation_action",
        )
    )
    admin.add_view(
        UrbanisAction(
            AppEnum,
            db.session,
            "Action Urbanis",
            url="urbanis-action",
            endpoint="manage_urbanis_action",
        )
    )
    admin.add_view(
        LitigationAction(
            AppEnum,
            db.session,
            "Action contentieuse",
            url="litigation-action",
            endpoint="manage_litigation_action",
        )
    )
    admin.add_view(
        ArchitectQualification(
            AppEnum,
            db.session,
            "Qualification de l'architecte",
            url="architect-qualification",
            endpoint="manage_architect_qualification",
        )
    )
    admin.add_view(
        SecurityCommissionResult(
            AppEnum,
            db.session,
            "Résultats du comité de sécurité",
            url="security-commission-result",
            endpoint="manage_security_commission_result",
        )
    )
    admin.add_view(
        LocalisationCopropriete(
            AppEnum,
            db.session,
            "Localisation de la copropriete",
            url="localisation-copropriete",
            endpoint="manage_localisation_copropriete",
        )
    )
    admin.add_view(
        WaterBillingType(
            AppEnum,
            db.session,
            "Modalités de facturation d'eau",
            url="water-billing-type",
            endpoint="manage_water_billing_type",
        )
    )
    admin.add_view(
        HeaterBillingType(
            AppEnum,
            db.session,
            "Modalités de facturation du chauffage",
            url="heater-billing-type",
            endpoint="manage_heater_billing_type",
        )
    )
    admin.add_view(
        MeetingTheme(
            AppEnum,
            db.session,
            "Thème - réunions",
            url="meeting-theme",
            endpoint="manage_meeting_theme",
        )
    )
    admin.add_view(
        ActionUrbanisThemeGUP(
            AppEnum,
            db.session,
            "Thème - action Urbanis au titre de la GUP",
            url="action-urbanis-theme-gup",
            endpoint="manage_action_urbanis_theme_gup",
        )
    )
    admin.add_view(
        OtherActionUrbanis(
            AppEnum,
            db.session,
            "Thème - autre action à laquelle participe Urbanis",
            url="other-action-urbanis",
            endpoint="manage_other_action_urbanis",
        )
    )
    admin.add_view(
        NatureDysfunction(
            AppEnum,
            db.session,
            "Dysfonctionnement (nature)",
            url="dysfunction-nature",
            endpoint="manage_dysfunction_nature",
        )
    )
    admin.add_view(
        ActionType(
            AppEnum,
            db.session,
            "Type d'action",
            url="action-type",
            endpoint="manage_action_type",
        )
    )
    admin.add_view(
        CommunicationActionType(
            AppEnum,
            db.session,
            "Type d'action de communication",
            url="communication-action-type",
            endpoint="manage_communication_action_type",
        )
    )
    admin.add_view(
        ActionResponsibleCommunication(
            AppEnum,
            db.session,
            "Responsable de l'action - communication",
            url="action-responsible-communication",
            endpoint="manage_action_responsible_communication",
        )
    )
    admin.add_view(
        FormationType(
            AppEnum,
            db.session,
            "Modalités de la formation",
            url="formation-type",
            endpoint="manage_formation_type",
        )
    )
    admin.add_view(
        Former(
            AppEnum,
            db.session,
            "Formateur",
            url="former",
            endpoint="manage_former",
        )
    )
    admin.add_view(
        ActionResponsibleFormation(
            AppEnum,
            db.session,
            "Responsable de l'action - formation",
            url="action-responsible-formation",
            endpoint="manage_action_responsible_formation",
        )
    )
    admin.add_view(
        AGType(
            AppEnum,
            db.session,
            "Type d'AG",
            url="ag-type",
            endpoint="manage_ag_type",
        )
    )
    admin.add_view(
        Renegociation(
            AppEnum,
            db.session,
            "Renégociation",
            url="renegociation",
            endpoint="manage_renegociation",
        )
    )
    admin.add_view(
        CompetitionReopening(
            AppEnum,
            db.session,
            "Remise en concurrence",
            url="competition-reopening",
            endpoint="manage_competition_reopening",
        )
    )
    admin.add_view(
        ConsumptionLabel(
            AppEnum,
            db.session,
            "Etiquette de consommation",
            url="consumption-label",
            endpoint="manage_consumption_label",
        )
    )
    admin.add_view(
        ProcedureCommonParts(
            AppEnum,
            db.session,
            "Procédures administratives - parties communes",
            url="procedures-common-parts",
            endpoint="manage_procedures_common_parts",
        )
    )
    admin.add_view(
        ProcedurePrivateParts(
            AppEnum,
            db.session,
            "Procédures administratives - parties privatives",
            url="procedures-private-parts",
            endpoint="manage_procedures_private_parts",
        )
    )
    admin.add_view(
        WorkNatureAssetPlan(
            AppEnum,
            db.session,
            "Nature des travaux - plan de patrimoine",
            url="work-nature-asset-plan",
            endpoint="manage_work_nature_asset_plan",
        )
    )
    admin.add_view(
        WorkEligibleSubsidiesHeritagePlan(
            AppEnum,
            db.session,
            "Travaux recevables aux subventions - plan de patrimoine",
            url="work-eligible-subsidies-heritage-plan",
            endpoint="manage_work_eligible_subsidies_heritage_plan",
        )
    )
    admin.add_view(
        ActionResponsible(
            AppEnum,
            db.session,
            "Responsable de l'action",
            url="action-responsible",
            endpoint="manage_action_responsible",
        )
    )
    admin.add_view(
        WorkNatureCommonParts(
            AppEnum,
            db.session,
            "Nature des travaux sur Parties Communes",
            url="work-nature-common-parts",
            endpoint="manage_work_nature_common_parts",
        )
    )
    admin.add_view(
        WorkNatureCollectivInterestPrivateParts(
            AppEnum,
            db.session,
            "Nature des Travaux d'Intérêt Collectif sur Parties Privatives",
            url="work-nature-collectiv-interest-private-parts",
            endpoint="manage_work_nature_collectiv_interest_private_parts",
        )
    )
    admin.add_view(
        HelpType(
            AppEnum,
            db.session,
            "Type d'aide",
            url="help-type",
            endpoint="manage_help_type",
        )
    )
    admin.add_view(
        IndividualLoanType(
            AppEnum,
            db.session,
            "Type de prêt individuel - travaux hors AG",
            url="individual-loan-type",
            endpoint="manage_individual_loan_type",
        )
    )
    admin.add_view(
        WorkNaturePrivateParts(
            AppEnum,
            db.session,
            "Nature des travaux en PP",
            url="work-nature-private-parts",
            endpoint="manage_work_nature_private_parts",
        )
    )
    admin.add_view(
        FunderOrganism(
            AppEnum,
            db.session,
            "Organisme financeur",
            url="funder-organism",
            endpoint="manage_funder_organism",
        )
    )
    admin.add_view(
        SupportingStructure(
            AppEnum,
            db.session,
            "Structure porteuse",
            url="supporting-structure",
            endpoint="manage_supporting_structure",
        )
    )
    admin.add_view(
        BuyerSales(
            AppEnum,
            db.session,
            "Acquéreur vente",
            url="buyer-sales",
            endpoint="manage_buyer_sales",
        )
    )
    admin.add_view(
        NatureSuivi(
            AppEnum,
            db.session,
            "Nature du suivi",
            url="nature-suivi",
            endpoint="manage_nature_suivi",
        )
    )
    admin.add_view(
        FSLType(
            AppEnum,
            db.session,
            "Type de FSL",
            url="fsl-type",
            endpoint="manage_fsl_type",
        )
    )
    admin.add_view(
        AccompaniementClosing(
            AppEnum,
            db.session,
            "Clôture de l'accompagnement",
            url="accompaniement-closing",
            endpoint="manage_accompaniement_closing",
        )
    )
