from app.repositories.base_repo import BaseRepo
from app.models.user_skill import UserSkill


class UserSkillRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserSkill)

    def new_user_skill(self, skill_level, years, skill_id, user_id, is_deleted=False):
        new_user_skill = UserSkill(
            skill_level=skill_level,
            years=years,
            skill_id=skill_id,
            is_deleted=is_deleted,
            user_id=user_id,
        )

        new_user_skill.save()
        return new_user_skill
