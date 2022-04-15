"""empty message

Revision ID: 9ad87acb91aa
Revises: b8ac6ad1b7a1
Create Date: 2022-04-14 13:14:44.852959

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9ad87acb91aa'
down_revision = 'b8ac6ad1b7a1'
branch_labels = None
depends_on = None

existing_enums = {
    "CombinedStructureType": [
        "AFUL",
        "ASL",
        "Union de syndicats"
    ],
    "LotOccupantStatus": [
        "Propriétaire",
        "Locataire",
        "Sous locataire",
        "Occupant à titre gratuit",
        "Occupant sans droit ni titre",
        "Bail meublé",
        "Bail expiré",
        "Lot vacant",
        "Location saisonnière courte durée ",
        "Résidence secondaire ",
        "Autre"
    ]
}

enums_T2_T3_T6 = {
        "WorkAxis": [
            "Scission",
            "Résidentialisation",
            "Fusion",
            "Autre"
        ],
        "MainOccupantAge": [
            "20-30",
            "31-40",
            "41-60",
            "61-75"
            "> 75",
            "NR"
        ],
        "HouseholdDebtRate": [
            "0-33",
            "33-50",
            "> 50",
            "NR"
        ],
        "LotSeniorityOccupation": [
            "< 1 an",
            "1-5 ans",
            "5-10 ans",
            "> 10 ans",
            "NR"
        ],
        "RentLevel": [
            "LCTS de fait",
            "LCTS conventionné",
            "LCS de fait",
            "LCS conventionné",
            "LI de fait",
            "LI conventionné",
            "NR"
        ],
        "HouseholdResourcesAnahStatus": [
            "< PO TM",
            "PO M",
            "> plafonds ANAH",
            "NR"
        ],
        "HouseholdOtherFunderLimitStatus": [
            "< plafonds",
            "> plafonds",
            "NR"
        ],
        "LocatairesRessources": [
            "< PLAI",
            "< PLUS",
            "< PLS",
            "< LI",
            "> LI",
            "NR"
        ],
        "HouseholdEnergeticEffortRate": [
            "0-5",
            "5-10",
            ">10",
            "NR"
        ],
        "EnergeticPrecariousnessCause": [
            "Usage",
            "Revenus",
            "Qualité du logement",
            "Qualité de l''immeuble",
            "NR"
        ],
        "Overoccupation": [
            "non",
            "oui sur critères nb de piéces",
            "oui sur critères CAF",
            "oui aigue",
            "NR"
        ],
        "HouseholdAccompaniedStatusAndPreviousStatus": [
            "Propriétaire",
            "Locataire",
            "Sous-locataire",
            "Hebergé",
            "Sans droit ni titre",
            "Bailleur",
            "Autre",
            "NR"
        ],
        "AdministrativeSituation": [
            "Carte d''identité française",
            "Passeport européen",
            "Titre de séjour 1 an",
            "Carte de résident",
            "Absence de titre",
            "Autre"
        ],
        "MaritalSituation": [
            "Marié-e",
            "Séparé-e",
            "Divorcé-e",
            "Célibataire",
            "Union libre",
            "Pacs-é",
            "Veuf-ve",
            "Autre",
            "NR"
        ],
        "MovingHouseProject": [
            "0-1",
            "1-5",
            "5-10",
            "> 10",
            "NR"
        ],
        "MonthlyRessourcesType": [
            "Salaire",
            "Indemnité chômage",
            "IJ",
            "RSA",
            "Retraite",
            "Prestations Familiales",
            "Pension invalidité",
            "Pension alimentaire",
            "Pension de reversion"
            "AAH",
            "Prime Activité",
            "Autre"
        ],
        "DebtOrigin": [
            "Perte emploi",
            "Pas une priorité",
            "Refus de régler",
            "Méconnaissance",
            "Difficultés budgétaires",
            "NR"
        ],
        "PrincipalSocialProblematics": [
            "Difficulté financière",
            "Difficulté pour payer quote-part travaux",
            "Dette de charges",
            "Procédure Expulsion",
            "Procédure Saisie Immo",
            "Situation sur-occupation",
            "Inadaptation Logement",
            "Conflit Loc/PB",
            "Risque Saturnin",
            "Abs Droits ouverts"
        ],
        "SocialSupportType": [
            "URBANIS",
            "SSD",
            "CCAS",
            "CAF",
            "Autre"
        ],
        "RDVType": [
            "domicile / visio / permanence ou local",
            "visio",
            "permanence ou local"
        ],
        "AdministrativeSupport": [
            "Aide financière type alimentaire",
            "FSL",
            "FSE-FSeau",
            "Aide 1% ",
            "CAF",
            "CNAV",
            "FAP Subvention",
            "FAP Prêt",
            "PAH ",
            "Autre"
        ],
        "InformativeEventsOrganization": [
            "Réunion cage d''escaliers",
            "Réunion pied d''immeuble",
            "Réunion générale",
            "Fête des voisins",
            "Autre"
        ],
        "ProfessionalSituation": [
            "Salarié",
            "Fonctionnaire",
            "Travailleur Indépendant",
            "Demandeur d''emploi",
            "Retraité",
            "Invalidité",
            "Autre"
        ],
        "ContractType": [
            "CDI temps plein",
            "CDI temps partiel",
            "CDD temps plein",
            "CDD temps partiel",
            "Interimaire",
            "Formation rémunérée",
            "Formation non rémunérée",
            "Autre"
        ],
        "PreLitigationAction": [
            "Relance",
            "Mise en demeure",
            "Sommation d''huissier",
            "Relance par avocat",
            "Commandement de payer",
            "Prise d''hypothèque",
            "Autre",
            "NR"
        ],
        "UrbanisAction": [
            "Echéancier",
            "Aides financières",
            "Accompagnement à la vente",
            "Commission de suivi des impayés",
            "Autre",
            "NR"
        ],
        "LitigationAction": [
            "Assignation ",
            "Audience",
            "Rendu du jugement",
            "Exécution forcée du jugement",
            "Commandement de payer valant saisie immobilière",
            "Saisie immobilière portée au vote",
            "Saisie immobilière votée",
            "Vente immobilière effectuée",
            "Autre",
            "NR"
        ]
    }

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Merge existing enums
    for (kind, values) in existing_enums.items():
        for value in values:
            # Check if name already exists
            res = session.execute(f"SELECT name FROM core.enum WHERE kind = '{kind}' AND name = '{value}'")
            found = False
            for _ in res:
                found = True
            if not found:
                # Add it if not
                session.execute(
                    "INSERT INTO core.enum (created_at, updated_at, kind, name, display_order, disabled, private) VALUES "
                    f"('{now}', '{now}', '{kind}', '{value}', NULL, false, false)"
                )

    # Add not existing enums
    for (kind, values) in enums_T2_T3_T6.items():
        for value in values:
            session.execute(
                "INSERT INTO core.enum (created_at, updated_at, kind, name, display_order, disabled, private) VALUES "
                f"('{now}', '{now}', '{kind}', '{value}', NULL, false, false);"
            )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)
    # Remove not existing enums
    for (kind, values) in enums_T2_T3_T6.items():
        for value in values:
            session.execute(
                f"DELETE FROM core.enum WHERE kind = '{kind}' AND name = '{value}';"
            )