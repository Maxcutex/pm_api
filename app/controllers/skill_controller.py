from app.controllers.base_controller import BaseController
from app.repositories.skill_repo import SkillRepo


class SkillController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.skill_repo = SkillRepo()

    def list_skills(self):
        skills = self.skill_repo.get_unpaginated()
        skill_list = [skill.serialize() for skill in skills.items]
        return self.handle_response(
            "OK",
            payload={
                "skills": skill_list,
            },
        )

    def get_skill(self, skill_id):
        skill = self.skill_repo.find_first(id=skill_id)
        if skill:
            return self.handle_response("OK", payload={"skill": skill.serialize()})
        return self.handle_response("Invalid or Missing skill_id", status_code=400)

    def create_skill(self):
        name, skill_category_id = self.request_params("name", "skill_category_id")
        skill = self.skill_repo.find_first(
            name=name, skill_category_id=skill_category_id
        )

        if skill:
            print("testing ....")
            return self.handle_response(
                f"Skill name {skill.name} with category name {skill.skill_category.name} already exists",
                status_code=400,
            )
        skill = self.skill_repo.new_skill(
            name=name, skill_category_id=skill_category_id
        )

        return self.handle_response(
            "OK", payload={"skill": skill.serialize()}, status_code=201
        )

    def update_skill(self, update_id):
        skill_id, name, skill_category_id = self.request_params(
            "skill_id", "name", "skill_category_id"
        )
        skill = self.skill_repo.find_first(
            name=name, skill_category_id=skill_category_id
        )

        skill_other = self.skill_repo.get(name=name)

        if skill_id != update_id:
            return self.handle_response(
                "Invalid or incorrect skill_id provided", status_code=400
            )

        if skill:
            if skill.id == skill_other.id:
                skill = self.skill_repo.update(
                    skill, **dict(name=name, skill_category_id=skill_category_id)
                )
                return self.handle_response(
                    "OK", payload={"skill": skill.serialize()}, status_code=200
                )
            else:
                return self.handle_response(
                    f"Skill name '{name}' with category name {skill_other.skill_category.name} already exists",
                    status_code=400,
                )
        return self.handle_response("Skill Not Found", status_code=404)

    def delete_skill(self, skill_id):
        skill = self.skill_repo.get(skill_id)
        update_dict = {"is_deleted": True}
        if skill:
            self.skill_repo.update(**update_dict)
            return self.handle_response("skill deleted", payload={"status": "success"})
        return self.handle_response(
            "Invalid or incorrect skill_id provided", status_code=404
        )
