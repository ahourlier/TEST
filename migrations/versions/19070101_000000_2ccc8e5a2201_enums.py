"""enums

Revision ID: 2ccc8e5a2201
Revises: 480d8160e141
Create Date: 2020-05-12 14:26:13.293144

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2ccc8e5a2201"
down_revision = "0a8c88e769ce"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    enum_table = op.create_table(
        "enum",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("kind", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=True),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("private", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("kind", "name", name=op.f("pk_enum")),
        schema="core",
    )

    initial_enums = {
        "MissionStatus": ["Non débutée", "En cours", "Post opération", "Archivée"],
        "ProjectStatus": [
            "À Contacter",
            "Contact",
            "Visite conseil à programmer",
            "Visite conseil programmée",
            "Visite à traiter",
            "En cours de montage",
            "Déposé",
            "Agréé",
            "Visite contrôle à programmer",
            "Visite contrôle programmée",
            "Demande paiement à faire",
            "En demande de paiement",
            "Soldé",
            "Sans suite",
            "Non éligible",
        ],
        "ProjectContactSource": [
            "ANAH",
            "Artisans",
            "Bouche à oreille",
            "Collectivité",
            "Communication",
            "Opérateur",
            "Partenaires (CAF, CCAS...)",
            "Autre",
        ],
        "ProjectRequesterType": [
            "PO",
            "PB",
            "Locataire",
            "SDC (Syndicat des Copropriétaires",
        ],
        "ProjectCaseType": [
            "Habiter Mieux Sérénité",
            "Adaptation",
            "Travaux Lourds",
            "Sécurité et Salubrité de l'Habitat",
            "Mixte",
            "Transformation d'usage",
            "Caisse de retraite",
            "Action Logement/Energie",
            "Action Logement/Adaptation",
            "Autre",
            "Aucun",
        ],
        "ProjectIneligibilityCause": [
            "Hors plafond",
            "Vente",
            "PTZ Acquisition",
            "Projet non éligible",
            "Travaux démarrés",
            "Autre dispositif",
            "Précédent dossier ANAH",
            "Autre",
        ],
        "ProjectWorksType": [
            "Isolation toiture",
            "Isolation murs",
            "Isolation autre",
            "Menuiseries",
            "Chauffage",
            "ECS",
            "Ventilation",
            "Adaptation salle de bain",
            "Adaptation création unité de vie",
            "Toiture",
            "Electricité",
            "Assainissement",
            "Structure",
            "Sanitaire",
            "Rénovation globale",
            "Autre",
        ],
        "ProjectClosureMotiveType": ["Abandon", "Vente", "Décès", "Autre"],
        "ProjectAccommodationType": [
            "Maison",
            "Appartement",
            "Immeuble",
            "Local commercial",
            "Autre",
        ],
        "FunderType": [
            "Etat",
            "Région",
            "Département",
            "EPCI",
            "Commune",
            "Caisse de retraite",
            "CAF",
            "Autre subvention publique",
            "Autre subvention privée",
        ],
    }

    rows = []
    current_date = datetime.utcnow()
    for kind, items in initial_enums.items():
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

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("enum", schema="core")
    # ### end Alembic commands ###