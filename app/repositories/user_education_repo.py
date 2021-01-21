from app.repositories.base_repo import BaseRepo
from app.models.user_education import UserEducation


class UserEducationRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserEducation)

    def new_user_education(
        self,
        user_id,
        institution_name,
        course_name,
        degree_earned,
        accomplishments,
        institution_city,
        institution_country,
        start_date,
        end_date,
    ):
        user_education = UserEducation(
            institution_name=institution_name,
            course_name=course_name,
            degree_earned=degree_earned,
            accomplishments=accomplishments,
            institution_city=institution_city,
            institution_country=institution_country,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
        )
        user_education.save()
        return user_education
