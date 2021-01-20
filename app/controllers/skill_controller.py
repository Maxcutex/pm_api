from app.controllers.base_controller import BaseController
from app.repositories.skill_repo import SkillRepo


class SkillController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.skill_repo = SkillRepo()

    def list_skills(self):
        skills = self.skill_repo.fetch_all()
        if skills:
            skill_list = [skill.serialize() for skill in skills.items]
            return self.handle_response(
                "OK",
                payload={
                    "skills": skill_list,
                    "meta": self.pagination_meta(skills),
                },
            )
        return self.handle_response("Empty dataset", status_code=400)

    def get_skill(self, skill_id):
        skill = self.skill_repo.get(skill_id)
        if skill:
            return self.handle_response("OK", payload={"skill": skill.serialize()})
        return self.handle_response("Invalid or Missing skill_id", status_code=400)

    def create_skill(self):
        name, skill_category_id = self.request_params("name", "skill_category_id")
        skill = self.skill_repo.new_skill(
            name=name, skill_category_id=skill_category_id
        )

        return self.handle_response(
            "OK", payload={"skill": skill.serialize()}, status_code=201
        )

    def update_skill(self, skill_id):
        name, skill_category_id = self.request_params("name", "skill_category_id")
        skill = self.skill_repo.get(skill_id)
        if skill:
            skill = self.skill_repo.update(skill, **dict(name=name, skill_category_id=skill_category_id))
            return self.handle_response(
                "OK", payload={"skill": skill.serialize()}, status_code=201
            )
        return self.handle_response("Location Not Found", status_code=404)


    def delete_skill(self, skill_id):
        skill = self.skill_repo.get(skill_id)
        update_dict ={"is_deleted": True}
        if skill:
            self.skill_repo.update(**update_dict)
            return self.handle_response("role deleted", payload={"status": "success"})
        return self.handle_response(
            "Invalid or incorrect role_id provided", status_code=404
        )