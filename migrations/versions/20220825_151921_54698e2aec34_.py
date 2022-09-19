"""empty message

Revision ID: 54698e2aec34
Revises: 46116ada951e
Create Date: 2022-08-25 15:19:21.174471

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "54698e2aec34"
down_revision = "46116ada951e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "urbanis_collaborators",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_in_charge_id", sa.Integer(), nullable=True),
        sa.Column("copro_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["copro_id"],
            ["core.copro.id"],
            name=op.f("fk_urbanis_collaborators_copro_id_copro"),
        ),
        sa.ForeignKeyConstraint(
            ["user_in_charge_id"],
            ["core.user.id"],
            name=op.f("fk_urbanis_collaborators_user_in_charge_id_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_urbanis_collaborators")),
        schema="core",
    )
    op.drop_constraint(
        "fk_copro_user_in_charge_id_user", "copro", schema="core", type_="foreignkey"
    )
    op.drop_column("copro", "user_in_charge_id", schema="core")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "copro",
        sa.Column(
            "user_in_charge_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        schema="core",
    )
    op.create_foreign_key(
        "fk_copro_user_in_charge_id_user",
        "copro",
        "user",
        ["user_in_charge_id"],
        ["id"],
        source_schema="core",
        referent_schema="core",
    )
    op.drop_table("urbanis_collaborators", schema="core")
    # ### end Alembic commands ###