from collections import OrderedDict

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from termcolor import colored

from app.models import (
    Location,
    Role,
    UserRole,
    Permission,
    User,
    Skill,
    SkillCategory,
    UserEmployment,
    UserEmploymentSkill,
    UserProjectSkill,
    UserProject,
    UserEducation,
    UserSkill,
)
from app.utils import db
from .seed_data import (
    location_data,
    permission_data,
    role_data,
    user_data,
    user_role_data,
    skill_data,
    skill_category_data,
    user_employment_data,
    user_employment_skill_data,
    user_project_data,
    user_education_data,
    user_project_skill_data,
    user_skill_data,
)
from .test_data import test_data

SEED_OPTIONS = ("location", "role", "user_role", "permission", "user")
model_mapper = OrderedDict(
    {
        "location": {"model": Location, "data": location_data},
        "role": {"model": Role, "data": role_data},
        "user": {"model": User, "data": user_data},
        "user_role": {"model": UserRole, "data": user_role_data},
        "permission": {"model": Permission, "data": permission_data},
        "skill_category": {"model": SkillCategory, "data": skill_category_data},
        "skill": {"model": Skill, "data": skill_data},
        "user_employment": {"model": UserEmployment, "data": user_employment_data},
        "user_skill": {"model": UserSkill, "data": user_skill_data},
        "user_employment_skill": {
            "model": UserEmploymentSkill,
            "data": user_employment_skill_data,
        },
        "user_education": {"model": UserEducation, "data": user_education_data},
        "user_project": {"model": UserProject, "data": user_project_data},
        "user_project_skill": {
            "model": UserProjectSkill,
            "data": user_project_skill_data,
        },
    }
)


def check_start_insert_condition(start_insert, table_name, name):

    if start_insert:
        start_insert = False if table_name == name else True

    return start_insert


def truncate_db():

    for table in reversed(model_mapper):
        try:
            query = "TRUNCATE table {} RESTART IDENTITY CASCADE".format(
                model_mapper.get(table).get("model").__tablename__
            )
            db.engine.execute(text(query))
            print(query)

        except OperationalError:
            query = "DELETE FROM {}".format(
                model_mapper.get(table).get("model").__tablename__
            )
            db.engine.execute(text(query))
            print(query)


def bulk_insert(model, data):
    try:
        db.session.bulk_insert_mappings(model, data)
        # for each_data in data:
        #     user = User(first_name=each_data.first_name)
        #     db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception(colored(error, "red"))


def seed_db(table_name, testing):
    start_insert = True

    truncate_db()

    for name, model in model_mapper.items():
        if testing:
            model["data"].extend(test_data.get(name, []))
        if start_insert:
            bulk_insert(**model)

        start_insert = check_start_insert_condition(start_insert, table_name, name)
