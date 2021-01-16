import datetime

from app.controllers.base_controller import BaseController
from app.repositories import SkillRepo, UserProjectSkillRepo, UserProjectRepo, UserRepo


class UserProjectController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_repo = UserRepo()
        self.user_project_repo = UserProjectRepo()
        self.user_project_skill_repo = UserProjectSkillRepo()
        self.skill_repo = SkillRepo()

    def _get_project_skills(self, project_id):
        skills_list = []
        skills = self.user_project_skill_repo.get_unpaginated(
            user_project_id=project_id
        )
        for skill in skills:
            skill_data = self.skill_repo.find_first(id=skill)
            skill_dict = skill_data.serialize()
            skill_dict["name"] = skill_data.name
            skills_list.append(skill_dict)
        return skills_list

    def list_user_projects(self, user_id):
        user_projects = self.user_project_repo.get_unpaginated(user_id=user_id)

        user_project_list = []
        for user_project in user_projects:
            user_project_dict = user_project.serialize()
            user_project_dict["skills"] = self._get_project_skills(user_project.id)
            user_project_list.append(user_project_dict)
        return self.handle_response(
            "OK",
            payload={
                "user_projects": user_project_list,
            },
        )

    def get_user_project(self, user_project_id):
        user_project = self.user_project_repo.get(user_project_id)

        if user_project:
            user_project_dict = user_project.serialize()
            user_project_dict["skills"] = self._get_project_skills(user_project.id)
            return self.handle_response(
                "OK", payload={"user_project": user_project_dict}
            )
        return self.handle_response(
            "Invalid User Project or Missing user_project_id", status_code=400
        )

    def create_user_project(self):
        (
            user_id,
            project_name,
            project_url,
            project_description,
            start_date,
            end_date,
            is_current,
            skills,
        ) = self.request_params(
            "user_id",
            "project_name",
            "project_url",
            "project_description",
            "start_date",
            "end_date",
            "is_current",
            "skills",
        )
        try:

            if not isinstance(start_date, datetime.date):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            if start_date > end_date:
                return self.handle_response(
                    "Start Date cannot be greater than End date ", status_code=400
                )
            if skills is not None:
                self._validate_skills(skills)

            user_project = self.user_project_repo.new_user_project(
                user_id=user_id,
                project_name=project_name,
                project_url=project_url,
                project_description=project_description,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
            )
            skills_dict = self._process_skills(user_project.id, skills)

            user_project_serialized = user_project.serialize()
            user_project_serialized["skills"] = skills_dict
            return self.handle_response(
                "OK",
                payload={"user_project": user_project_serialized},
                status_code=201,
            )
        except Exception as e:
            return self.handle_response("Error processing: " + str(e), status_code=400)

    def _validate_skills(self, skills):
        for skill in skills:
            skill_data = self.skill_repo.find_first(id=skill)
            if skill_data is None:
                return self.handle_response(
                    "One of the skills is invalid", status_code=400
                )
        return

    def _process_skills(self, user_project_id, skills):
        skills_dict = []

        if skills is not None:

            for skill in skills:
                user_project_skills = (
                    self.user_project_skill_repo.new_user_project_skill(
                        user_project_id=user_project_id, skill_id=skill
                    )
                )
                skill_data = self.skill_repo.find_first(id=skill)
                user_project_skill_dict = user_project_skills.serialize()
                user_project_skill_dict["name"] = skill_data.name
                skills_dict.append(user_project_skill_dict)
        return skills_dict

    def update_user_project(self, update_id):
        (
            user_id,
            user_project_id,
            project_name,
            project_url,
            project_description,
            start_date,
            end_date,
            is_current,
            skills,
        ) = self.request_params(
            "user_id",
            "user_project_id",
            "project_name",
            "project_url",
            "project_description",
            "start_date",
            "end_date",
            "is_current",
            "skills",
        )
        if update_id != user_project_id:
            return self.handle_response(
                "Invalid or incorrect user_project_id provided", status_code=400
            )

        if skills is not None:
            self._validate_skills(skills)

        user_project = self.user_project_repo.get(user_project_id)

        if not isinstance(start_date, datetime.date):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        if user_project:
            updates = {
                "project_name": project_name,
                "project_url": project_url,
                "project_description": project_description,
                "start_date": start_date,
                "end_date": end_date,
                "is_current": is_current,
            }

            self.user_project_repo.update(user_project, **updates)
            skills_dict = self._process_skills(user_project.id, skills)
            user_project_serialized = user_project.serialize()
            user_project_serialized["skills"] = skills_dict
            return self.handle_response(
                "OK",
                payload={"user_project": user_project_serialized},
            )

        return self.handle_response(
            "Invalid or incorrect user_project_id provided", status_code=400
        )

    def delete_user_project(self, user_project_id):
        user_project = self.user_project_repo.get(user_project_id)

        if user_project:
            updates = {"is_deleted": True}
            self.user_project_repo.update(user_project, **updates)
            return self.handle_response(
                "user project deleted", payload={"status": "success"}
            )
        return self.handle_response(
            "Invalid or incorrect user_project_id provided", status_code=404
        )
