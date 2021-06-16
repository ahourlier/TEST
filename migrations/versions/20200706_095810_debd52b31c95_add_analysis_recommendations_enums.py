"""add analysis/recommendations enums

Revision ID: debd52b31c95
Revises: c611cc7f5cdc
Create Date: 2020-07-06 09:58:10.226602

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

revision = "debd52b31c95"
down_revision = "c611cc7f5cdc"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("enum",))
    enum_table = Table("enum", meta)

    additional_enums = {
        "ProjectHeatingAnalysis": [
            "Présence de menuiseries simple vitrage",
            "Présence de menuiserie(s) double vitrage peu performante(s)",
            "Porte d'entrée simple vitrage",
            "Porte d'entrée peu isolante",
            "Combles perdus non isolés",
            "Combles perdus peu isolés",
            "Rampants de toiture non isolés",
            "Rampants de toiture faiblement isolés",
            "Toiture non isolée",
            "Toiture faiblement isolée",
            "Plancher bas non isolé",
            "Plancher bas faiblement isolé",
            "Murs extérieurs non isolés",
            "Murs extérieurs faiblement isolés",
            "Chaudière hors service",
            "Chaudière vétuste",
            "Installation de chauffage vétuste",
            "Installation de chauffage hors service",
            "Absence d'installation de chauffage suffisante",
            "Présence de convecteurs électriques peu efficaces",
            "Chauffage d'appoint iinsuffisante",
            "Absence de système de régulation du chauffage",
            "Chauffe-eau électrique vétuste",
            "Production d'eau chaude sanitaire peu performante",
            "Absence de ventilation",
            "Ventilation naturelle insuffisante",
            "Ventilation mécanique défectueuse",
            "Système de ventilation inadapté au logement",
            "Absence d'entrées d'air sur les menuiseries des pièces de vie",
        ],
        "ProjectAdaptationAnalysis": [
            "Salle de bain peu accessible",
            "Baignoire dont l'accès nécesssite un franchissement important",
            "Douche dont l'accès nécessite un franchissement",
            "Meuble vasque non adapté",
            "Absence de barres d'appui",
            "WC non réhaussé",
            "Largeur de porte insuffisante",
            "Accès au logement inadapté",
            "Escalier peu accessible",
            "Le logement ne dispose pas d'une unité de vie sur un même niveau",
        ],
        "ProjectTechnicalAnalysis": [
            "Menuiserie(s)  vétsutes et/ou dégradée(s)",
            "Porte d'entrée vétuste et/ou dégradée",
            "Présence de moisissure sur les menuiseries",
            "Présence de moisissure sur la porte d'entrée",
            "Revêtements de murs dégradés",
            "Revêtements de sols dégradés",
            "Revêtements de plafond dégradés",
            "Toiture vétuste",
            "Toiture vétsute avec infiltrations",
            "Inflitrations en toiture",
            "Suspicion de présence d'amiante",
            "Charpente dégradée",
            "Charpente vétuste",
            "Humidité tellurique",
            "Présence d'humidité",
            "Electricité vétuste",
            "Electricité vétuste et dangereuse",
            "Système d'assainissemet non conforme",
            "Présence de peintures dégradées susceptibles de contenir du plomb",
            "Présence de fissures en maçonnerie",
            "Joints de façade dégradés",
            "Appareils sanitaires manquants",
            "Appareils sanitaires défectueux",
            "Absence de détecteur(s) de fumée",
            "Absence de détecteur(s) de CO",
            "Installation de combustion non étanche incompatible avec la pose d'une VMC",
            "Installation gaz défectueuse",
            "Mains courantes manquantes ou défectueuses",
            "Absence de garde corps avec allège inférieure à 1 m",
        ],
        "ProjectHeatingRecommendation": [
            "Remplacement des menuiseries simple vitrage par des menuiseries double vitrage, "
            "avec Uw <= 1,3W/m².K et Sw > 0,3 ou Uw <= 1,7W/m².K et Sw > 0,36.",
            "Remplacement des menuiseries speu performantes par des menuiseries double vitrage, "
            "avec Uw <= 1,3W/m².K et Sw > 0,3 ou Uw <= 1,7W/m².K et Sw > 0,36.",
            "Remplacement de la porte d'entrée, avec Ud <= 1,7 W/m².K",
            "Remplacement de la porte, avec Ud <= 1,7W/m².K",
            "Isolation des combles perdus, avec R = 7m².K/W à minima",
            "Isolation des rampants de toiture, avec R = 6m².K/W à minima",
            "Isolation de la toiture terrasse, avec R = 4,5m².K/W à minima",
            "Isolation du plancher bas, avec R = 3m2.K/W à minima",
            "Isolation des murs extérieurs par l'intérieur, avec R = 3,7m².K/W à minima",
            "Isolation des murs extérieurs par l'extérieur, avec R = 3,7m².K/W à minima",
            "Remplacement de la chaudière par une chaudière à condensation",
            "Mise en oeuvre d'une installation de chauffage central avec chaudière à "
            "condensation, radiateurs basse température et régulation",
            "Remplacement de la chaudière par une pompe à chaleur air/eau",
            "Mise en oeuvre d'une pompe à chaleur air/eau",
            "Mise en oeuvre d'une pompe à chaleur air/air",
            "Mise en oeuvre d'un poêle à bois performant (Flamme Verte 7 étoiles ou performances "
            "équivalentes)",
            "Mise en oeuvre d'un insert performant (Flamme Verte 7 étoiles ou performances "
            "équivalentes)",
            "Mise en oeuvre d'un programmateur",
            "Mise en oeuvre de têtes thermostatiques sur les radiateurs",
            "Mise en oeuvre d'un chauffe-eau électrique performant",
            "Mise en oeuvre d'un chauffe-eau thermodynamique",
            "Couplage de la production d'eau chaude sanitaire à la production de chauffage",
            "Mise en oeuvre d'entrées d'air sur les menuiseries des pièces de vie",
            "Mise en oeuvre d'entrées d'air hygroréglables sur les menuiseries de pièces de vie",
            "Mise en oeuvre d'une VMC hygroréglable de type A",
            "Mise en oeuvre d'une VMC hygroréglable de type B",
            "Mise en oeuvre d'une VMC autoréglable",
            "Mise en oeuvre d'un extracteur hygroréglable et permanente",
            "Création de ventilations naturelles",
        ],
        "ProjectAdaptationRecommendation": [
            "Motorisation des volets",
            "Création d'une unité de vie",
            "Mise en oeuvre d'un revêtement de sol antidérapant",
            "Mise en oeuvre d'une douche sans ressaut, avec revêtement de sol anti-dérapant",
            "Mise en oeuvre d'une colonne de douche thermostatique accessible",
            "Mise en oeuvre d'un banc/d'un siège de douche",
            "Mise en oeuvre de barres d'appui",
            "Mise en oeuvre de mains courantes",
            "Mise en oeuvre d'une vasque accessible",
            "Mise en oeuvre d'un WC réhaussé",
            "Installation d'un monte-escalier",
            "Elargissement des passages de portes",
            "Mise en oeuvre d'une porte coulissante",
            "Mise en oeuvre d'une rampe d'accès au logement",
            "Aménagement du cheminement extérieur",
        ],
        "ProjectTechnicalRecommendation": [
            "Réhabilitation globale du logement",
            "Réfection des revêtements de murs",
            "Réfection des revêtements de sols",
            "Réfection des revêtements de plafonds",
            "Remplacement de la toiture",
            "Reprise partielle de la toiture",
            "Traitement des infiltrations en toiture",
            "Reprise partielle de la charpente",
            "Remplacement complet de la charpente",
            "Renforcement de la chapente",
            "Dépose des éléments amiantés",
            "Traitement de l'humidité tellurique par injections",
            "Mise en sécurité de l'installation électrique",
            "Réfection complète de l'installation électrique selon la norme NF C 15-100",
            "Mise en conformité du système d'assainissement",
            "Suppression des peintures contenant du plomb",
            "Recouvrement durable des peintures contenant du plomb",
            "Traitement des fissures en maçonnerie",
            "Rejointoiement de la façade",
            "Création d'un coin cuisine fonctionnel",
            "Création d'une salle de bain fonctionnelle",
            "Réfection de la salle de bain",
            "Mise en oeuvre de détecteurs de fumée",
            "Mise en oeuvre de détecteurs de CO",
            "Mise aux normes de l'installation gaz",
            "Création des ventilation nécessaires à l'installation de combustion",
            "Mise en oeuvre d'un robinet ROAI",
            "Suppression de l'installation de combustion dangereuse",
            "Mise en oeuvre de mains courantes",
            "Mise en oeuvre de gardes corps",
            "Traitement anti-termites",
        ],
    }

    rows = []
    current_date = datetime.utcnow()
    for kind, items in additional_enums.items():
        for i, name in enumerate(items):
            rows.append(
                {
                    "name": name,
                    "kind": kind,
                    "display_order": i + 1,
                    "private": True,
                    "disabled": False,
                    "created_at": current_date,
                    "updated_at": current_date,
                }
            )

    op.bulk_insert(
        enum_table, rows,
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "DELETE FROM core.enum WHERE kind = 'ProjectHeatingAnalysis' OR kind = "
        "'ProjectAdaptationAnalysis' OR kind = 'ProjectTechnicalAnalysis' OR kind = "
        "'ProjectHeatingRecommendation' OR kind = 'ProjectAdaptationRecommendation' OR kind = 'ProjectTechnicalRecommendation';"
    )
