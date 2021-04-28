"""add disorder_type table

Revision ID: 0a8c88e769ce
Revises: 09703cacc1ac
Create Date: 2020-05-06 11:00:51.980698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0a8c88e769ce"
down_revision = "480d8160e141"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "disorder_type",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_name", sa.String(length=255), nullable=False),
        sa.Column("is_analysis", sa.Boolean(), nullable=False),
        sa.Column("disorder_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["disorder_id"],
            ["core.disorder.id"],
            name=op.f("fk_disorder_type_disorder_id_disorder"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_disorder_type")),
        schema="core",
    )
    op.add_column(
        "disorder",
        sa.Column("analysis_localisation", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "disorder",
        sa.Column("recommendation_localisation", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.drop_column("disorder", "localisation", schema="core")
    op.drop_column("disorder", "analysis_type", schema="core")
    op.drop_column("disorder", "recommendation_type", schema="core")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "disorder",
        sa.Column(
            "recommendation_type",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=True,
        ),
        schema="core",
    )
    op.add_column(
        "disorder",
        sa.Column(
            "analysis_type", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "disorder",
        sa.Column(
            "localisation", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
        schema="core",
    )
    op.drop_column("disorder", "recommendation_localisation", schema="core")
    op.drop_column("disorder", "analysis_localisation", schema="core")
    op.drop_table("disorder_type", schema="core")
    # ### end Alembic commands ###
