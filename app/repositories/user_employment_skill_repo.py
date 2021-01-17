from app.repositories.base_repo import BaseRepo
from app.models.user_employment_skill import UserEmploymentSkill


class UserEmploymentSkillRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserEmploymentSkill)

    def new_user_employment_skill(self, user_employment_id, skill_id):
        user_employment_skill = UserEmploymentSkill(
            user_employment_id=user_employment_id,
            skill_id=skill_id,
        )
        user_employment_skill.save()
        return user_employment_skill
