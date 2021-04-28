"""recreate accommodation

Revision ID: f6e588288616
Revises: c04231341a73
Create Date: 2020-04-20 11:52:07.664626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f6e588288616"
down_revision = "c04231341a73"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accommodation",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("accommodation_type", sa.String(length=255), nullable=True),
        sa.Column("condominium", sa.Boolean(), nullable=True),
        sa.Column("purchase_year", sa.Date(), nullable=True),
        sa.Column("construction_year", sa.Date(), nullable=True),
        sa.Column("levels_nb", sa.Integer(), nullable=True),
        sa.Column("rooms_nb", sa.Integer(), nullable=True),
        sa.Column("living_area", sa.Float(), nullable=True),
        sa.Column("additional_area", sa.Float(), nullable=True),
        sa.Column("vacant", sa.Boolean(), nullable=True),
        sa.Column("year_vacant_nb", sa.Integer(), nullable=True),
        sa.Column("commentary", sa.String(length=800), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_accommodation")),
        schema="core",
    )
    op.add_column(
        "disorder",
        sa.Column("accommodation_id", sa.Integer(), nullable=False),
        schema="core",
    )
    op.create_foreign_key(
        op.f("fk_disorder_accommodation_id_accommodation"),
        "disorder",
        "accommodation",
        ["accommodation_id"],
        ["id"],
        source_schema="core",
        referent_schema="core",
    )
    op.add_column(
        "project",
        sa.Column("accommodation_id", sa.Integer(), nullable=True),
        schema="core",
    )
    op.create_unique_constraint(
        op.f("uq_project_accommodation_id"),
        "project",
        ["accommodation_id"],
        schema="core",
    )
    op.create_foreign_key(
        op.f("fk_project_accommodation_id_accommodation"),
        "project",
        "accommodation",
        ["accommodation_id"],
        ["id"],
        source_schema="core",
        referent_schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_project_accommodation_id_accommodation"),
        "project",
        schema="core",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("uq_project_accommodation_id"), "project", schema="core", type_="unique"
    )
    op.drop_column("project", "accommodation_id", schema="core")
    op.drop_constraint(
        op.f("fk_disorder_accommodation_id_accommodation"),
        "disorder",
        schema="core",
        type_="foreignkey",
    )
    op.drop_column("disorder", "accommodation_id", schema="core")
    op.drop_table("accommodation", schema="core")
    # ### end Alembic commands ###
