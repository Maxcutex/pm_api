"""empty message

Revision ID: 4e41bd179702
Revises: 3bf61cf107f2
Create Date: 2021-01-16 12:22:45.967900

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4e41bd179702"
down_revision = "3bf61cf107f2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_project_skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("user_project_id", sa.Integer(), nullable=True),
        sa.Column("skill_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_project_id"],
            ["user_projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("user_projects", sa.Column("end_date", sa.Date(), nullable=False))
    op.add_column("user_projects", sa.Column("is_current", sa.Boolean(), nullable=True))
    op.add_column(
        "user_projects", sa.Column("project_description", sa.Text(), nullable=False)
    )
    op.add_column(
        "user_projects", sa.Column("project_name", sa.String(), nullable=False)
    )
    op.add_column(
        "user_projects", sa.Column("project_url", sa.String(), nullable=False)
    )
    op.add_column("user_projects", sa.Column("start_date", sa.Date(), nullable=False))
    op.add_column("user_projects", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "user_projects", "users", ["user_id"], ["id"])
    op.drop_column("user_projects", "gender")
    op.drop_column("user_projects", "date_of_birth")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_projects",
        sa.Column("date_of_birth", sa.DATE(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "user_projects",
        sa.Column(
            "gender",
            postgresql.ENUM("male", "female", name="gender"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_constraint(None, "user_projects", type_="foreignkey")
    op.drop_column("user_projects", "user_id")
    op.drop_column("user_projects", "start_date")
    op.drop_column("user_projects", "project_url")
    op.drop_column("user_projects", "project_name")
    op.drop_column("user_projects", "project_description")
    op.drop_column("user_projects", "is_current")
    op.drop_column("user_projects", "end_date")
    op.drop_table("user_project_skills")
    # ### end Alembic commands ###