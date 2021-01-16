from app.repositories.base_repo import BaseRepo
from app.models.user_project_skill import UserProjectSkill


class UserProjectSkillRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserProjectSkill)

    def new_user_project_skill(self, user_project_id, skill_id):
        user_project_skill = UserProjectSkill(
            user_project_id=user_project_id,
            skill_id=skill_id,
        )
        user_project_skill.save()
        return user_project_skill
