"""Set updated_at to created_at when null

Revision ID: 55e4a31e1790
Revises: c43dc508a276
Create Date: 2020-04-17 08:39:30.952246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "55e4a31e1790"
down_revision = "c43dc508a276"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    tables = (
        "agency",
        "antenna",
        "client",
        "contact",
        "document",
        "mission",
        "permission",
        "phone_number",
        "project",
        "project_lead",
        "requester",
        "role",
        "taxable_income",
        "team",
        "user",
        "user_group",
    )

    for table in tables:
        connection.execute(
            f"""
            UPDATE core.{table} SET updated_at = created_at WHERE updated_at is NULL
            """
        )


def downgrade():
    pass
