from app.repositories.base_repo import BaseRepo
from app.models.skill import Skill


class SkillRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, Skill)

    def new_skill(self, name, skill_category_id):
        skill = Skill(name=name, skill_category_id=skill_category_id)

        skill.save()
        return skill
