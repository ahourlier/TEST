"""empty message

Revision ID: 18f0c5cfdcf7
Revises: 27454aa2af37
Create Date: 2022-05-12 09:50:57.266679

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '18f0c5cfdcf7'
down_revision = '27454aa2af37'
branch_labels = None
depends_on = None

enums = {
    "LocalisationCopropriete": [
        "Centre-ville",
        "Banlieue",
        "Péri-urbain"
    ],
    "WaterBillingType": [
        "Collectif",
        "Compteur individuel",
        "Abonnement individuel"
    ],
    "MeetingTheme": [
        "Gestion des déchets",
        "Stationnement",
        "Propreté",
        "Nuisibles",
        "Sécurité et tranquillité publiques",
        "Lien social",
        "Articulation avec le projet urbain"
    ],
    "ActionUrbanisThemeGUP": [
        "Gestion des déchets",
        "Stationnement",
        "Propreté",
        "Nuisibles",
        "Sécurité et tranquillité publiques",
        "Lien social",
        "Articulation avec le projet urbain"
    ],
    "OtherActionUrbanis": [
        "Activité économique",
        "Citoyenneté",
        "Culture",
        "Education",
        "Lutte contre les discriminations",
        "Lutte contre lles violences sociales",
        "Emploi / insertion par l''économique",
        "Illétrisme / illétronisme",
        "Pauvreté",
        "Santé",
        "Sports"
    ],
    "NatureDysfunction": [
        "Globe",
        "Ampoule",
        "Interrupteur",
        "Portes halls",
        "Portes coupe-feu",
        "Panneau affichage",
        "Poubelles halls",
        "Ascenseur",
        "Boîte lettres",
        "Dépôts sauvages parkings",
        "Propreté halls",
        "Propreté paliers",
        "Locaux OM",
        "Espaces verts",
        "Dépôts sauvages espaces communs extérieurs",
        "Dépôts sauvages point collecte encombrants",
        "Propreté ascenseur",
        "Tags",
        "Encombrants palier",
        "Encombrants placard technique",
        "Encombrants balcons",
        "Epaves / ventouses",
        "Mécanique sauvage",
        "Stationnement gênant espace public",
        "Occupation PC extérieures",
        "Occupation PC intérieures",
        "Troubles voisinage",
        "Squatt halls",
        "Squatt logements",
        "Autre"
    ],
    "ActionType": [
        "Réunion cage d''escaliers",
        "Réunion pied d''immeuble",
        "Réunion générale",
        "Autre"
    ],
    "CommunicationActionType": [
        "Affichage",
        "Boîtage",
        "Article",
        "Autre"
    ],
    "ActionResponsibleCommunication": [
        "Urbanis",
        "Co-traitant / sous-traitant",
        "Partenaire institutionnel",
        "Client",
        "Organisme spécialisé tiers",
        "Syndic / AP",
        "CS",
        "Personnel d''immeuble",
        "Autre"
    ],
    "FormationType": [
        "Formation présentielle",
        "Formation distancielle",
        "Formation hybride",
        "Autre"
    ],
    "Former": [
        "Urbanis",
        "Co-traitant / sous-traitant",
        "Partenaire institutionnel",
        "Client",
        "Organisme spécialisé tiers",
        "Autre"
    ],
    "ActionResponsibleFormation": [
        "Urbanis",
        "Co-traitant / sous-traitant",
        "Partenaire institutionnel",
        "Client",
        "Organisme spécialisé tiers",
        "Syndic / AP",
        "CS",
        "Autre"
    ],
    "ActionResponsible": [
        "Urbanis",
        "Co-traitant / sous-traitant",
        "Partenaire institutionnel",
        "Client",
        "Organisme spécialisé tiers",
        "Syndic / AP",
        "CS",
        "Personnel d''immeuble",
        "Autre"
    ],
    "AGType": [
        "AGO",
        "AGE",
        "AGS",
        "Réunion AP"
    ],
    "Renegociation": [
        "Négociation aboutie",
        "Négociation non aboutie",
        "Amélioration du service rendu à coût équivalent"
    ],
    "CompetitionReopening": [
        "Remise en concurrence aboutie",
        "Remise en concurrence non aboutie",
        "Amélioration du service rendu à coût équivalent"
    ],
    "ConsumptionLabel": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "Non calculé",
        "Non renseigné"
    ],
    "ProcedureCommonParts": [
        "Mise en conformité avec les normes de décence",
        "Logements ou parcelles encombrés",
        "Danger sanitaire ponctuel",
        "Traitement de l''insalubrité",
        "Traitement des risques structurels",
        "Dangers liés aux équipements communs",
        "Traitement des situations d''urgence",
        "Etablissement d''hébergement / ERP",
        "Immeubles en état d''abandon manifeste",
        "Immeubles sans propriétaire connu",
        "Permis de louer",
        "Permis de diviser",
        "Polices antérieures à l''ordonnance du 16/09/20",
        "Injonction de ravalement",
        "Article 123 du CSP",
        "Arrêté de péril",
        "Autre"
    ],
    "ProcedurePrivateParts": [
        "Mise en conformité avec les normes de décence",
        "Logements encombré",
        "Danger sanitaire ponctuel",
        "Traitement de l''insalubrité",
        "Traitement des risques structurels",
        "Traitement des situations d''urgence",
        "Etablissement d''hébergement / ERP",
        "Permis de louer",
        "Permis de diviser",
        "Polices antérieures à l''ordonnance du 16/09/20",
        "Article 123 du CSP",
        "Arrêté de péril",
        "Infraction au RSD",
        "Autre"
    ],
    "WorkNatureAssetPlan": [
        "Travaux préparatoires",
        "Gros oeuvre",
        "Toiture, charpente, couverture",
        "Réseaux, équipements sanitaires",
        "Chauffage, production d''eau chaude, système de refroidissement ou climatisation",
        "Production d''énergie décentralisée",
        "Ventilation",
        "Mensuieries extérieures",
        "Ravalement, étanchéité, isolation extérieure",
        "Revêtements intérieurs, étanchéité, isolation thermique et acoustique",
        "Traitements spécifiques (plomb, amiante, radon, xylophages, nuisibles)",
        "Ascenseur, monte-personne",
        "Sécurité incendie",
        "Aménagements intérieurs",
        "Chemins extérieurs, cours, passages, locaux communs",
        "Extension de logements, création de locaux annexes",
        "Travaux d''entretien d''ouvrages existants",
        "Renforcement lié aux risques naturels",
        "Renforcement lié aux risques technologiques",
        "Maîtrise d''oeuvre",
        "Diagnostics",
        "Contrats d''entretien"
    ],
    "WorkEligibleSubsidiesHeritagePlan": [
        "Oui",
        "Non",
        "Partiellement"
    ],
    "WorkNatureCommonParts": [
        "Travaux préparatoires",
        "Gros oeuvre",
        "Toiture, charpente, couverture",
        "Réseaux, équipements sanitaires",
        "Chauffage, production d''eau chaude, système de refroidissement ou climatisation",
        "Production d''énergie décentralisée",
        "Ventilation",
        "Menuiseries extérieures",
        "Ravalement, étanchéité, isolation extérieure",
        "Revêtements intérieurs, étanchéité, isolation thermique et acoustique",
        "Traitements spécifiques (plomb, amiante, radon, xylophages, nuisibles)",
        "Ascenseur, monte-personne",
        "Sécurité incendie",
        "Aménagements intérieurs",
        "Chemins extérieurs, cours, passages, locaux communs",
        "Extension de logements, création de locaux annexes",
        "Travaux d''entretien d''ouvrages existants",
        "Renforcement lié aux risques naturels",
        "Renforcement lié aux risques technologiques",
        "Autre"
    ],
    "WorkNatureCollectiveInterestPrivateParts": [
        "Travaux d''isolation thermique des parois vitrées donnant sur l''extérieur comprenant, le cas échéant, l''installation de systèmes d''occultation extérieurs",
        "Pose ou remplacement d''organes de régulation ou d''équilibrage sur les émetteurs de chaleur ou de froid",
        "Equilibrage des émetteurs de chaleur ou de froid",
        "Mise en place d''équipements de comptage des quantités d''énergies consommées"
    ],
    "HelpType": [
        "Aide au SDC",
        "Aide mixte",
        "Dossier mandataire commun",
        "Aides individuelles"
    ],
    "IndividualLoanType": [
        "Eco-PTZ",
        "Prêt missions sociales",
        "Prêt avance mutation / rénovation",
        "Prêt personnel copropriété ",
        "Prêt copropriétés dégradées",
        "Autre prêt individuel"
    ],
    "WorkNaturePrivateParts": [
        "Travaux préparatoires",
        "Gros oeuvre",
        "Toiture, charpente, couverture",
        "Réseaux, équipements sanitaires",
        "Chauffage, production d''eau chaude, système de refroidissement ou climatisation",
        "Production d''énergie décentralisée",
        "Ventilation",
        "Menuiseries extérieures",
        "Ravalement, étanchéité, isolation extérieure",
        "Revêtements intérieurs, étanchéité, isolation thermique et acoustique",
        "Traitements spécifiques (plomb, amiante, radon, xylophages, nuisibles)",
        "Ascenseur, monte-personne",
        "Sécurité incendie",
        "Aménagements intérieurs",
        "Chemins extérieurs, cours, passages, locaux communs",
        "Extension de logements, création de locaux annexes",
        "Travaux d''entretien d''ouvrages existants",
        "Renforcement lié aux risques naturels",
        "Renforcement lié aux risques technologiques",
        "Autre"
    ],
    "FunderOrganism": [
        "Anah",
        "Ville",
        "Intercommunalité",
        "Département",
        "Région ",
        "Caisse de retraite",
        "MDPH",
        "Fondation Abbé Pierre",
        "Action logement",
        "Autre"
    ],
    "SupportingStructure": [
        "CDC Habitat",
        "EPF",
        "Action Logement Immobilier",
        "Organisme HLM",
        "Autre"
    ],
    "BuyerSales": [
        "Locataire en place",
        "Bailleur social",
        "CDC Habitat",
        "Collecteur 1%",
        "Autre"
    ]
}

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    # Add not existing enums
    for (kind, values) in enums.items():
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
    for (kind, values) in enums.items():
        for value in values:
            session.execute(
                f"DELETE FROM core.enum WHERE kind = '{kind}' AND name = '{value}';"
            )
    # ### end Alembic commands ###
