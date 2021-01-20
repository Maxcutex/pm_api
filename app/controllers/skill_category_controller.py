from app.controllers.base_controller import BaseController
from app.repositories.skill_category_repo import SkillCategoryRepo
from app.utils.redisset import RedisSet


class SkillCategoryController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.skill_category_repo = SkillCategoryRepo()
        self.redis_set = RedisSet()

    def list_skills_categories(self):
        skills_categories = self.skill_category_repo.filter_by(is_deleted=False)

        skills_category_list = [
            skills_category.serialize() for skills_category in skills_categories.items
        ]
        return self.handle_response(
            "OK",
            payload={
                "skills_categories": skills_category_list,
                "meta": self.pagination_meta(skills_categories),
            },
        )

    def get_skills_category(self, skills_category_id):
        skills_category = self.skill_category_repo.get(skills_category_id)
        if skills_category:
            return self.handle_response(
                "OK", payload={"skills_category": skills_category.serialize()}
            )
        return self.handle_response(
            "Invalid or Missing skills_category_id", status_code=400
        )

    def create_skills_category(self):
        name, help_ = self.request_params("name", "help")
        skills_category1 = self.skill_category_repo.find_first(name=name)

        if not skills_category1:
            try:
                skills_category = self.skill_category_repo.new_skill_category(
                    name=name, help_=help_
                )
                return self.handle_response(
                    "OK",
                    payload={"skills_category": skills_category.serialize()},
                    status_code=201,
                )
            except Exception as e:
                return self.handle_response(
                    "Error processing: " + str(e), status_code=400
                )

        return self.handle_response(
            "Skills Category with this name already exists", status_code=400
        )

    def update_skills_category(self, update_id):
        name, help_, skill_category_id = self.request_params(
            "name", "help", "skill_category_id"
        )

        if update_id != skill_category_id:
            return self.handle_response(
                "Invalid or incorrect skills_category_id provided", status_code=400
            )
        skills_category = self.skill_category_repo.get(skill_category_id)
        if skills_category:
            updates = {}
            if name:
                skills_category1 = self.skill_category_repo.find_first(name=name)
                if skills_category1:
                    return self.handle_response(
                        "Skills Category with this name already exists", status_code=400
                    )
                updates["name"] = name
            if help_:
                updates["help"] = help_

            skills_category = self.skill_category_repo.update(
                skills_category, **updates
            )
            return self.handle_response(
                "OK", payload={"skills_category": skills_category.serialize()}
            )
        return self.handle_response(
            "Invalid or incorrect skills_category_id provided", status_code=400
        )

    def delete_skills_category(self, skills_category_id):
        skills_category = self.skill_category_repo.get(skills_category_id)
        if skills_category:
            updates = {}
            updates["is_deleted"] = True
            self.skill_category_repo.update(skills_category, **updates)
            return self.handle_response(
                "skills category deleted", payload={"status": "success"}
            )
        return self.handle_response(
            "Invalid or incorrect skills_category_id provided", status_code=404
        )

    def autocomplete(self):
        params = self.get_params("q")
        rows = []
        if params:
            for value in self.redis_set.get(params[0]):
                if value:
                    rows.append(value)
        return self.handle_response(rows, status_code=200)
