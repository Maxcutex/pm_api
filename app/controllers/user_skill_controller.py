import datetime

from app.controllers.base_controller import BaseController
from app.repositories import SkillRepo, UserRepo
from app.repositories.user_skill_repo import UserSkillRepo


class UserSkillController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_repo = UserRepo()
        self.user_skill_repo = UserSkillRepo()
        self.skill_repo = SkillRepo()

    def list_user_skills(self, user_id):
        user_skills = self.user_skill_repo.get_unpaginated(user_id=user_id)

        user_skill_list = []
        for user_skill in user_skills:
            user_skill_dict = user_skill.serialize()
            user_skill_list.append(user_skill_dict)
        return self.handle_response(
            "OK",
            payload={
                "user_skills": user_skill_list,
            },
        )

    def get_user_skill(self, user_skill_id):
        user_skill = self.user_skill_repo.get(user_skill_id)

        if user_skill:
            user_skill_dict = user_skill.serialize()
            return self.handle_response("OK", payload={"user_skill": user_skill_dict})
        return self.handle_response(
            "Invalid User Project or Missing user_skill_id", status_code=400
        )

    def create_user_skill(self):
        (skill_level, years, skill_id, user_id,) = self.request_params(
            "skill_level",
            "years",
            "skill_id",
            "user_id",
        )
        try:

            skill_data = self.skill_repo.find_first(id=skill_id)

            if skill_data is None:
                return self.handle_response("Skill Id is invalid", status_code=400)
            user_skill = self.user_skill_repo.new_user_skill(
                skill_level=skill_level, years=years, skill_id=skill_id, user_id=user_id
            )

            return self.handle_response(
                "OK",
                payload={"user_skill": user_skill.serialize()},
                status_code=201,
            )
        except Exception as e:
            return self.handle_response("Error processing: " + str(e), status_code=400)

    def update_user_skill(self, update_id):
        (user_id, user_skill_id, skill_level, years, skill_id,) = self.request_params(
            "user_id",
            "user_skill_id",
            "skill_level",
            "years",
            "skill_id",
        )
        if update_id != user_skill_id:
            return self.handle_response(
                "Invalid or incorrect user_skill_id provided", status_code=400
            )
        skill_data = self.skill_repo.find_first(id=skill_id)
        if skill_data is None:
            return self.handle_response("Skill Id is invalid", status_code=400)

        user_skill = self.user_skill_repo.find_first(id=update_id)

        if user_skill:
            updates = {
                "skill_level": skill_level,
                "years": years,
                "skill_id": skill_id,
                "user_id": user_id,
            }

            user_skill = self.user_skill_repo.update(user_skill, **updates)
            return self.handle_response(
                "OK",
                payload={"user_skill": user_skill.serialize()},
            )

        return self.handle_response(
            "Invalid or incorrect user_skill_id provided", status_code=400
        )

    def delete_user_skill(self, user_skill_id):
        user_skill = self.user_skill_repo.get(user_skill_id)

        if user_skill:
            updates = {"is_deleted": True}
            self.user_skill_repo.update(user_skill, **updates)
            return self.handle_response(
                "user skill deleted", payload={"status": "success"}
            )
        return self.handle_response(
            "Invalid or incorrect user_skill_id provided", status_code=404
        )
