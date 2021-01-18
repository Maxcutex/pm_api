from app.controllers.base_controller import BaseController
from app.repositories.skill_repo import SkillRepo


class SkillController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.skill_repo = SkillRepo()

    def list_skills(self):
        skills = self.skill_repo.fetch_all()
        skill_list = [skill.serialize() for skill in skills.items]
        return self.handle_response(
            "OK",
            payload={
                "skills": skill_list,
                "meta": self.pagination_meta(skills),
            },
        )

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
