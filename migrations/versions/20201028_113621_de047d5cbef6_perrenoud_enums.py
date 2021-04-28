""" perrenoud enums

Revision ID: de047d5cbef6
Revises: 8482c51c1664
Create Date: 2020-10-28 11:36:21.479188

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "de047d5cbef6"
down_revision = "8482c51c1664"
branch_labels = None
depends_on = None


def upgrade():
    # 1, 4, 5, 6, 7, 9, 10, 12, 15, 16, 17, 18, 19, 20
    # 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 31bis(77),
    # 32, 33, 36, 37, 51, 62, 63, 76

    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("perrenoud_enum_kind",))
    enum_perrenoud_kind_table = Table("perrenoud_enum_kind", meta)
    perrenoud_enums_key_labels = {
        1: "Altitude",
        4: "Inertie",
        5: "Position mur",
        6: "U connu",
        7: "Composition et épaisseur en cm des murs",
        9: "Paroi isolée",
        10: "Type d'isolation Mur",
        12: "Valeur connue pour l'isolant",
        15: "Type de local pour calcul de b",
        16: "Position plancher",
        17: "Composition plancher",
        18: "Type d'isolation plancher",
        19: "Position plafond",
        20: "Composition plafond",
        21: "Type d'isolation Plafond",
        22: "Type de menuiserie",
        23: "Matériaux menuiserie",
        24: "Type de vitrage",
        25: "Remplissage",
        26: "Epaisseur lame (air ou argon)",
        27: "Fermeture",
        30: "Inclinaison menuiserie",
        31: "Type de paroi vitree",
        312: "Choix type menuiserie porte / fenêtre",
        32: "Porte - Nature menuiserie",
        33: "Porte - Type de porte",
        36: "Position laison ME/Plancher intermédiaire",
        37: "Position laison ME/Refend",
        51: "Position Instantannée ou Accumulée",
        62: "Type de ventilation",
        63: "Type de Climatisation",
        76: "Type de pont thermique",
    }

    current_date = datetime.utcnow()
    rows = []
    for index, label in perrenoud_enums_key_labels.items():
        rows.append(
            {
                "index": index,
                "label": label,
                "created_at": current_date,
                "updated_at": current_date,
            }
        )

    op.bulk_insert(
        enum_perrenoud_kind_table, rows,
    )


def downgrade():
    pass
