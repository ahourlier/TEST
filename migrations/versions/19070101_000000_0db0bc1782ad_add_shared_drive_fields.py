"""Add Shared Drive fields

Revision ID: 0db0bc1782ad
Revises: fdeeec0ae386
Create Date: 2020-06-09 08:28:20.887569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0db0bc1782ad"
down_revision = "7c034e3842cf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "mission",
        sa.Column(
            "sd_document_templates_folder_id", sa.String(length=255), nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "mission",
        sa.Column(
            "sd_information_documents_folder_id", sa.String(length=255), nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "mission",
        sa.Column("sd_projects_folder_id", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "mission",
        sa.Column("sd_root_folder_id", sa.String(length=255), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("mission", "sd_root_folder_id", schema="core")
    op.drop_column("mission", "sd_projects_folder_id", schema="core")
    op.drop_column("mission", "sd_information_documents_folder_id", schema="core")
    op.drop_column("mission", "sd_document_templates_folder_id", schema="core")
    # ### end Alembic commands ###
