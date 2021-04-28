""" All remaining perrenoud enums

Revision ID: bde507b73ff1
Revises: de047d5cbef6
Create Date: 2020-10-28 12:24:40.290381

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "bde507b73ff1"
down_revision = "de047d5cbef6"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("perrenoud_enum",))
    perrenoud_enums = Table("perrenoud_enum", meta)

    new_perrenoud_enums = {
        1: [
            {"value": 1, "label": "inférieure à 400 m"},
            {"value": 2, "label": "entre 401 m et 800 m"},
            {"value": 3, "label": "entre 801 m et 1200 m"},
            {"value": 4, "label": "entre 1201 m et 1600 m"},
            {"value": 5, "label": "entre 1601 m et 2000 m"},
            {"value": 6, "label": "au dessus de 2000 m"},
        ],
        4: [
            {"value": 1, "label": "Légère"},
            {"value": 2, "label": "Moyenne"},
            {"value": 3, "label": "Lourde"},
            {"value": 4, "label": "Très Lourde"},
        ],
        5: [
            {"value": 0, "label": "Mur extérieur"},
            {"value": 1, "label": "Mur sur local non chauffé"},
        ],
        6: [
            {"value": 0, "label": "U calcul suivant méthode"},
            {"value": 1, "label": "U connu"},
        ],
        7: [
            {"value": 0, "label": "Inconnu"},
            {
                "value": 100,
                "label": "Murs en pierre de taille moellons (constitués d'un seul matériau) : <= 20",
            },
            {
                "value": 102,
                "label": "Murs en pierre de taille moellons (constitués d'un seul matériau) : 40",
            },
            {
                "value": 104,
                "label": "Murs en pierre de taille moellons (constitués d'un seul matériau) : 50",
            },
            {
                "value": 106,
                "label": "Murs en pierre de taille moellons (constitués d'un seul matériau) : 60",
            },
            {
                "value": 108,
                "label": "Murs en pierre de taille moellons (constitués d'un seul matériau) : 70",
            },
            {
                "value": 110,
                "label": "Murs en pierre de taille moellons (constitués d'un seul matériau) : 80",
            },
            {
                "value": 112,
                "label": "Murs en pierre de taille moellons (constitués avec remplissage tout venant) : 50",
            },
            {
                "value": 200,
                "label": "Murs en pierre de taille moellons (constitués avec remplissage tout venant) : 60",
            },
            {
                "value": 202,
                "label": "Murs en pierre de taille moellons (constitués avec remplissage tout venant) : 70",
            },
            {
                "value": 204,
                "label": "Murs en pierre de taille moellons (constitués avec remplissage tout venant) : 80",
            },
            {
                "value": 206,
                "label": "Mur en pisé ou béton de terre stabilisé (à partir d'argile crue) : <= 40",
            },
            {
                "value": 300,
                "label": "Mur en pisé ou béton de terre stabilisé (à partir d'argile crue) : 50",
            },
            {
                "value": 302,
                "label": "Mur en pisé ou béton de terre stabilisé (à partir d'argile crue) : 60",
            },
            {
                "value": 304,
                "label": "Mur en pisé ou béton de terre stabilisé (à partir d'argile crue) : 70",
            },
            {
                "value": 306,
                "label": "Mur en pisé ou béton de terre stabilisé (à partir d'argile crue) : 80",
            },
            {"value": 308, "label": "Mur en pans de bois avec remplissage : <= 8"},
            {"value": 600, "label": "Mur en pans de bois avec remplissage : 10"},
            {"value": 601, "label": "Mur en pans de bois avec remplissage : 13"},
            {"value": 602, "label": "Mur en pans de bois avec remplissage : 18"},
            {"value": 603, "label": "Mur en pans de bois avec remplissage : 24"},
            {"value": 604, "label": "Mur en pans de bois avec remplissage : 32"},
            {"value": 605, "label": "Mur en briques pleines simples : 12"},
            {"value": 701, "label": "Mur en briques pleines simples : 23"},
            {"value": 704, "label": "Mur en briques pleines simples : 34"},
            {"value": 900, "label": "Mur en briques pleines simples : 45"},
            {"value": 902, "label": "Mur en briques pleines simples : 60"},
            {"value": 904, "label": "Mur en briques creuses : <= 15"},
            {"value": 907, "label": "Mur en briques creuses : 20"},
            {"value": 908, "label": "Mur en briques creuses : 25"},
            {"value": 1100, "label": "Mur en briques creuses : 38"},
            {"value": 1102, "label": "Mur en briques creuses : 43"},
            {"value": 1200, "label": "Murs en blocs de béton creux : 25"},
            {"value": 1202, "label": "Mur en béton banché : <= 20"},
            {"value": 1204, "label": "Mur en béton banché : 25"},
            {"value": 1206, "label": "Mur en béton banché : 30"},
            {"value": 1300, "label": "Mur en béton banché : 40"},
            {"value": 1301, "label": "Mono mur : 30"},
            {"value": 1402, "label": "Mono mur : 37,5"},
            {"value": 1407, "label": "Mur en béton cellulaire : 20"},
            {"value": 1409, "label": "Mur en béton cellulaire : 37,5"},
            {"value": 1900, "label": "Cloison de plâtre : Inconnue"},
            {"value": 2000, "label": "Mur en béton de mâchefer : <= 20"},
            {"value": 2004, "label": "Mur en béton de mâchefer : 30"},
            {"value": 2006, "label": "Mur en béton de mâchefer : 40"},
        ],
        9: [{"value": 0, "label": "Non"}, {"value": 1, "label": "Oui"}],
        10: [
            {"value": 0, "label": "Par l'intérieur (ITI)"},
            {"value": 1, "label": "Par l'extérieur (ITE)"},
            {"value": 2, "label": "Répartie (ITR)"},
        ],
        12: [
            {"value": 0, "label": "R Isolant"},
            {"value": 1, "label": "Epaisseur de l'isolant"},
        ],
        15: [
            {"value": 0, "label": "Maison individuelle - Garage"},
            {"value": 1, "label": "Maison individuelle - Cellier"},
            {"value": 2, "label": "Maison individuelle - Véranda"},
            {"value": 3, "label": "Maison individuelle - Comble fortement ventilé"},
            {"value": 4, "label": "Maison individuelle - Comble faiblement ventilé"},
            {"value": 5, "label": "Maison individuelle - Sous-sol"},
            {
                "value": 6,
                "label": "Collectif Circulations communes sans ouverture directe sur l'extérieur",
            },
            {
                "value": 7,
                "label": "Collectif Circulations communes avec ouverture directe sur l'extérieur",
            },
        ],
        16: [
            {"value": 0, "label": "Sur terre-plein"},
            {"value": 1, "label": "Sur vide-sanitaire"},
            {"value": 2, "label": "Sur local non chauffé"},
            {"value": 3, "label": "Sur local autre que d'habitation"},
            {"value": 4, "label": "Sur l'extérieur"},
        ],
        17: [
            {"value": 1, "label": "Type de plancher inconnu"},
            {"value": 2, "label": "Plancher avec ou sans remplissage"},
            {
                "value": 3,
                "label": "Plancher entre solives bois avec ou sans remplissage",
            },
            {"value": 4, "label": "Bardeaux et remplissage"},
            {"value": 5, "label": "Plancher bois sur solives bois"},
            {
                "value": 6,
                "label": "Plancher entre solives métalliques avec ou sans remplissage",
            },
            {"value": 7, "label": "Plancher bois sur solives métalliques"},
            {"value": 8, "label": "Voutains sur solives métalliques"},
            {
                "value": 9,
                "label": "Plancher lourd type, entrevous terre-cuite, poutrelles béton",
            },
            {"value": 10, "label": "Dalle de béton"},
            {"value": 11, "label": "Voutains en briques ou moellons"},
            {"value": 13, "label": "Plancher à entrevous isolants"},
        ],
        18: [
            {"value": 0, "label": "Sous chape (ITI)"},
            {"value": 1, "label": "En sous face (ITE)"},
            {"value": 2, "label": "ITI+ITE"},
        ],
        19: [
            {"value": 0, "label": "Terrasse"},
            {"value": 1, "label": "Combles aménagés"},
            {"value": 2, "label": "Sur local non chauffé (combles perdus,...)"},
            {"value": 3, "label": "Sur local autre que d'habitation"},
        ],
        20: [
            {"value": 0, "label": "Plafond inconnu"},
            {"value": 1, "label": "Plafond en plaque de plâtre"},
            {"value": 3, "label": "Plafond bois sur solives bois"},
            {"value": 4, "label": "Bardeaux et remplissage"},
            {
                "value": 5,
                "label": "Plafond entre solives bois avec ou sans remplissage",
            },
            {"value": 6, "label": "Plafond bois sur solives métalliques"},
            {"value": 7, "label": "Plafond bois sous solives métalliques"},
            {
                "value": 8,
                "label": "Entres solives métalliques, avec ou sans remplissage",
            },
            {"value": 9, "label": "Entrevous terre-cuite ou poutrelles en béton"},
            {"value": 10, "label": "Dalle de béton"},
            {"value": 11, "label": "Combles aménagés sous rampant"},
            {"value": 12, "label": "Toiture en chaume"},
            {"value": 14, "label": "Plafond bois sous solives bois"},
            {"value": 15, "label": "Plafond avec ou sans remplissage"},
        ],
        21: [
            {"value": 0, "label": "Par l'intérieur (ITI)"},
            {"value": 1, "label": "Par l'extérieur (ITE)"},
            {"value": 2, "label": "Répartie (ITR)"},
        ],
        22: [
            {"value": 0, "label": "Fenêtre battante"},
            {"value": 1, "label": "Porte fenêtre sans sous bassement"},
            {"value": 2, "label": "Porte fenêtre avec sous bassement"},
            {"value": 3, "label": "Fenêtre coulissante"},
            {"value": 4, "label": "Porte fenêtre coulissante"},
        ],
        23: [
            {"value": 0, "label": "Bois ou bois métal"},
            {"value": 1, "label": "PVC"},
            {"value": 2, "label": "Métal"},
            {"value": 3, "label": "Métal avec rupture de P. Th."},
        ],
        24: [
            {"value": 0, "label": "Simple vitrage"},
            {"value": 1, "label": "Simple vitrage + survitrage"},
            {"value": 2, "label": "Double Vitrage"},
            {"value": 3, "label": "Triple Vitrage"},
        ],
        25: [
            {"value": 0, "label": "Air sec"},
            {"value": 1, "label": "Argon ou Krypton"},
        ],
        26: [
            {"value": 0, "label": "6"},
            {"value": 1, "label": "8"},
            {"value": 2, "label": "10"},
            {"value": 3, "label": "12"},
            {"value": 6, "label": "16"},
            {"value": 7, "label": "18"},
        ],
        27: [
            {"value": 7, "label": "Volet roulant Alu '7"},
            {"value": 8, "label": "Volet roulant PVC (e<=12mm) '8"},
            {"value": 9, "label": "Persienne coulissante (e<=22mm) '9"},
            {"value": 11, "label": "Volet battant bois (e<=22mm) '11"},
            {"value": 12, "label": "Volet roulant PVC (e>12mm) '12"},
            {"value": 13, "label": "Persienne coulissante (e>22mm) '13"},
            {"value": 14, "label": "Volet battant PVC (e>22mm) '14"},
            {"value": 15, "label": "Volet battant bois (e>22mm) '15"},
        ],
        30: [
            {"value": 0, "label": "Paroi verticale >=75°"},
            {"value": 1, "label": "Paroi horizontale <75°"},
        ],
        31: [
            {"value": 0, "label": "Fenêtre ou Porte-fenêtre"},
            {"value": 1, "label": "Briques de verre pleines"},
            {"value": 2, "label": "Briques de verre creuses"},
            {"value": 3, "label": "Paroi en polycarbonate"},
        ],
        312: [{"value": 0, "label": "Fenêtre"}, {"value": 1, "label": "Porte"}],
        32: [
            {"value": 0, "label": "Porte simple en bois"},
            {"value": 1, "label": "Porte simple en métal"},
            {"value": 2, "label": "Porte simple en PVC"},
            {"value": 3, "label": "Porte opaque pleine isolée"},
        ],
        33: [
            {"value": 0, "label": "Porte opaque pleine simple"},
            {"value": 1, "label": "Porte avec moins de 30% de vitrage simple"},
            {"value": 2, "label": "Porte avec 30-60% de vitrage simple"},
            {"value": 3, "label": "Porte avec double vitrage"},
        ],
        36: [
            {"value": 0, "label": "Entre 2 niveaux du projet"},
            {"value": 1, "label": "Plancher intermédiaire"},
        ],
        37: [
            {"value": 0, "label": "Entre 2 locaux du projet"},
            {"value": 1, "label": "Refend intermédiaire"},
        ],
        51: [
            {"value": 0, "label": "Instantanée"},
            {"value": 1, "label": "Accumulation"},
        ],
        62: [
            {"value": 0, "label": "Ventilation par ouverture des fenêtres"},
            {"value": 1, "label": "Ventilation par Entrées d'air hautes et basses"},
            {"value": 2, "label": "VMC SF Auto réglable avant 82"},
            {"value": 3, "label": "VMC SF Auto réglable après 82"},
            {"value": 4, "label": "VMC à extraction Hygro (Hygro A)"},
            {"value": 5, "label": "VMC Hygro Gaz"},
            {
                "value": 6,
                "label": "VMC Hygro à extraction et entrées d'air hygro (hygro B)",
            },
            {"value": 7, "label": "VMC Double Flux avec échangeur"},
            {"value": 9, "label": "Ventilation Naturelle par conduit"},
            {"value": 10, "label": "Ventilation Hybride"},
            {"value": 11, "label": "Mécanique sur conduit existant"},
            {
                "value": 12,
                "label": "Ventilation Naturelle par conduit avec entrées d'air hygro",
            },
            {"value": 13, "label": "Ventilation Hybride avec entrées d'air hygro"},
            {"value": 14, "label": "Puits climatique (canadien ou provençal)"},
        ],
        63: [
            {"value": 0, "label": "Aucun"},
            {"value": 1, "label": "Climatisation Electrique"},
            {"value": 2, "label": "Climatisation Gaz"},
        ],
        76: [
            {"value": 0, "label": "Mur ext / Plancher bas"},
            {"value": 1, "label": "Mur ext / Plafond"},
            {"value": 2, "label": "Mur ext / Plancher intermédiaire"},
            {"value": 3, "label": "Mur ext / Refend"},
        ],
        48: [
            {"value": 101, "label": "Electrique"},
            {
                "value": 102,
                "label": "Chauffe - eau thermo sur air ext.ou ambiant ou PAC double service",
            },
            {"value": 201, "label": "Générateur mixte(chauffage + ecs)"},
            {"value": 203, "label": "Accumulateur gaz"},
            {"value": 204, "label": "chauffe bain gaz instantané"},
        ],
        52: [{"value": 0, "label": "Vertical"}, {"value": 1, "label": "Horizontal"}],
        58: [
            {"value": 0, "label": "Avant 1990"},
            {"value": 1, "label": "De 1990 à 2000"},
            {"value": 2, "label": "Après 2000"},
        ],
        50: [
            {"value": 0, "label": "En volume habitable"},
            {"value": 1, "label": "Hors volume habitabl"},
        ],
        51: [
            {"value": 0, "label": "Instantanée"},
            {"value": 1, "label": "Accumulation"},
        ],
        60: [
            {"value": 0, "label": "Production ECS solaire"},
            {"value": 1, "label": "Système combiné chauffage / ECS solaire"},
        ],
    }
    current_date = datetime.utcnow()
    rows = []
    for index, items in new_perrenoud_enums.items():
        for item in items:
            rows.append(
                {
                    "index": index,
                    "value": item.get("value"),
                    "label": item.get("label"),
                    "created_at": current_date,
                    "updated_at": current_date,
                }
            )

    op.bulk_insert(
        perrenoud_enums, rows,
    )


def downgrade():
    pass
