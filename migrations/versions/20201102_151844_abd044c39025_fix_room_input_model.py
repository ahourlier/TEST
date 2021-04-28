"""fix room_input model

Revision ID: abd044c39025
Revises: 0a12122c7371
Create Date: 2020-11-02 15:18:44.931808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "abd044c39025"
down_revision = "0a12122c7371"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "room_input",
        "kind",
        existing_type=sa.BOOLEAN(),
        type_=sa.String(length=255),
        existing_nullable=True,
        schema="core",
    )
    op.drop_constraint(
        "fk_room_input_thermal_bridge_id_thermal_bridge",
        "room_input",
        schema="core",
        type_="foreignkey",
    )
    op.drop_column("room_input", "thermal_bridge_id", schema="core")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "room_input",
        sa.Column(
            "thermal_bridge_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        schema="core",
    )
    op.create_foreign_key(
        "fk_room_input_thermal_bridge_id_thermal_bridge",
        "room_input",
        "thermal_bridge",
        ["thermal_bridge_id"],
        ["id"],
        source_schema="core",
        referent_schema="core",
    )
    op.alter_column(
        "room_input",
        "kind",
        existing_type=sa.String(length=255),
        type_=sa.BOOLEAN(),
        existing_nullable=True,
        schema="core",
    )
    # ### end Alembic commands ###
