import datetime

from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from app.models import Skill, UserSkill
from app.repositories.base_repo import BaseRepo
from app.models.user import User


class UserRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, User)

    def new_user(
        self,
        first_name,
        last_name,
        email,
        gender,
        date_of_birth,
        location_id,
        password,
        employment_date=datetime.datetime.now().strftime("%Y-%m-%d"),
    ):
        """
        function for creating a new user



        """

        phash = generate_password_hash(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            date_of_birth=datetime.datetime.strptime(date_of_birth, "%Y-%m-%d"),
            location_id=location_id,
            password=phash,
            employment_date=datetime.datetime.strptime(employment_date, "%Y-%m-%d"),
        )
        user.save()
        return user

    def get_simple_search_paginated_options(self, search, page, per_page):
        return (
            User.query.filter(
                or_(
                    User.first_name.like(f"%{search}%"),
                    User.last_name.like(f"%{search}%"),
                    User.email.like(f"%{search}%"),
                )
            )
            .order_by(User.first_name.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    def get_advanced_search_paginated_options(
        self, experience, skills_list, location_id, page, per_page
    ):
        return (
            User.query.join(UserSkill, User.id == UserSkill.user_id)
            .filter(
                UserSkill.skill_id.in_(skills_list),
                location_id=location_id,
                experience_years=experience,
            )
            .order_by(User.first_name.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
