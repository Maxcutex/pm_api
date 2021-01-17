from app.repositories.base_repo import BaseRepo
from app.models.skill import Skill


class SkillRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, Skill)

    def new_skill(self, name, skill_category_id, is_active=True, is_deleted=False):
        new_skill = Skill(
            name=name,
            skill_category_id=skill_category_id,
            is_active=is_active,
            is_deleted=is_deleted,
        )

        new_skill.save()
        return new_skill
