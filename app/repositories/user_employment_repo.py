from app.repositories.base_repo import BaseRepo
from app.models.user_employment import UserEmployment


class UserEmploymentRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserEmployment)

    def new_user_employment(
        self, user_id, institution_name, job_title, start_date, end_date, is_current
    ):
        user_employment = UserEmployment(
            institution_name=institution_name,
            job_title=job_title,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            is_current=is_current,
        )
        user_employment.save()
        return user_employment
