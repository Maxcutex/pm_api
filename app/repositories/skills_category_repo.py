from app.repositories.base_repo import BaseRepo
from app.models.skills_category import SkillsCategory


class SkillsCategoryRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, SkillsCategory)

    def new_skills_category(self, name, help_=None, is_active=True, is_deleted=False):
        skills_category = SkillsCategory(
            name=name, help=help_, is_active=is_active, is_deleted=is_deleted
        )

        skills_category.save()
        return skills_category
