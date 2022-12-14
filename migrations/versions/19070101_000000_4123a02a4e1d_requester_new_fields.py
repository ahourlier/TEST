"""requester_new_fields

Revision ID: 4123a02a4e1d
Revises: 7ac45bcf6146
Create Date: 2020-06-30 15:00:05.177067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4123a02a4e1d"
down_revision = "7ac45bcf6146"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "requester",
        sa.Column("GIR_coefficient", sa.Integer(), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("company_name", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column(
            "disability_card", sa.Boolean(create_constraint=False), nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("have_AAH", sa.Boolean(create_constraint=False), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("have_APA", sa.Boolean(create_constraint=False), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("is_private", sa.Boolean(create_constraint=False), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("rate_adaptation", sa.Integer(), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("requester", "rate_adaptation", schema="core")
    op.drop_column("requester", "is_private", schema="core")
    op.drop_column("requester", "have_APA", schema="core")
    op.drop_column("requester", "have_AAH", schema="core")
    op.drop_column("requester", "disability_card", schema="core")
    op.drop_column("requester", "company_name", schema="core")
    op.drop_column("requester", "GIR_coefficient", schema="core")
    # ### end Alembic commands ###
