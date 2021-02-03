"""empty message

Revision ID: fd49af1e21e7
Revises: 4dbae139187c
Create Date: 2021-01-31 22:46:54.034056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fd49af1e21e7"
down_revision = "4dbae139187c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("institution_name", sa.String(), nullable=False),
        sa.Column("institution_url", sa.String(), nullable=True),
        sa.Column("institution_city", sa.String(), nullable=False),
        sa.Column("institution_country", sa.String(), nullable=False),
        sa.Column("institution_size", sa.String(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("lead", "closed", "rejected", name="clientstatus"),
            nullable=True,
        ),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("clients")
    # ### end Alembic commands ###