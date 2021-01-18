from app.repositories.base_repo import BaseRepo
from app.models.skill_category import SkillCategory


class SkillCategoryRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, SkillCategory)

    def new_skill_category(self, name, help_=None, is_active=True, is_deleted=False):
        skills_category = SkillCategory(
            name=name, help=help_, is_active=is_active, is_deleted=is_deleted
        )

        skills_category.save()
        return skills_category
