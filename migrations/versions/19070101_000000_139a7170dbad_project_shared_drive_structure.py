"""Project Shared Drive Structure

Revision ID: 139a7170dbad
Revises: cdf376d513be
Create Date: 2020-06-12 11:20:22.692687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "139a7170dbad"
down_revision = "cdf376d513be"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "project",
        sa.Column("sd_accommodation_folder_id", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column(
            "sd_accommodation_pictures_folder_id", sa.String(length=255), nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column(
            "sd_accommodation_report_folder_id", sa.String(length=255), nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("sd_funders_folder_id", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("sd_quotes_folder_id", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("sd_requester_folder_id", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("sd_root_folder_id", sa.String(length=255), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "sd_root_folder_id", schema="core")
    op.drop_column("project", "sd_requester_folder_id", schema="core")
    op.drop_column("project", "sd_quotes_folder_id", schema="core")
    op.drop_column("project", "sd_funders_folder_id", schema="core")
    op.drop_column("project", "sd_accommodation_report_folder_id", schema="core")
    op.drop_column("project", "sd_accommodation_pictures_folder_id", schema="core")
    op.drop_column("project", "sd_accommodation_folder_id", schema="core")
    # ### end Alembic commands ###