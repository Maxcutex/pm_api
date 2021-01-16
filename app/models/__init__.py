from sqlalchemy import event
from app.utils.id_generator import PushID

from .activity import Activity
from .permission import Permission
from .role import Role
from .user_role import UserRole
from .user import User
from .skill import Skill
from .skill_category import SkillCategory
from .user_education import UserEducation
from .user_employment import UserEmployment
from .user_employment_skill import UserEmploymentSkill
from .user_project import UserProject
from .user_project_skill import UserProjectSkill
from .user_skills import UserSkills
from .location import Location

__all__ = (
    "Role",
    "Permission",
    "UserRole",
    "Activity",
    "User",
    "SkillCategory",
    "Skill",
    "UserSkills",
    "UserProject",
    "UserProjectSkill",
    "UserEmploymentSkill",
    "UserEmployment",
    "UserEducation",
    "Location",
)

from .listener_helpers import attach_listen_type

tables_logged_after_every_insert = [
    UserEducation,
    UserEmployment,
    UserEmploymentSkill,
    UserProject,
    UserProjectSkill,
    UserSkills,
    Role,
    Permission,
    UserRole,
    User,
    Skill,
    SkillCategory,
    Location,
]
tables_logged_after_every_update = [
    UserEducation,
    UserEmployment,
    UserEmploymentSkill,
    UserProject,
    UserProjectSkill,
    UserSkills,
    Role,
    Permission,
    UserRole,
    User,
    Skill,
    SkillCategory,
    Location,
]
tables_logged_after_every_delete = [
    UserEducation,
    UserEmployment,
    UserEmploymentSkill,
    UserProject,
    UserProjectSkill,
    UserSkills,
    Role,
    Permission,
    UserRole,
    User,
    Skill,
    SkillCategory,
    Location,
]
generate_id_tables = (User,)

# attach all listeners to each admin table
attach_listen_type(tables_logged_after_every_insert, "after_insert")
attach_listen_type(tables_logged_after_every_update, "after_update")
attach_listen_type(tables_logged_after_every_delete, "after_delete")


def model_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    next_id = push_id.next_id()

    target.slack_id = target.slack_id if target.slack_id else next_id

    target.user_id = target.user_id if target.user_id else target.slack_id


# to be used if we are tying to slack. For now no.
# for table in generate_id_tables:
#     event.listen(table, 'before_insert', model_id_generator)
