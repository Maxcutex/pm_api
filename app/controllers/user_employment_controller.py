import datetime

from app.controllers.base_controller import BaseController
from app.repositories import (
    UserRepo,
    SkillRepo,
    UserEmploymentRepo,
    UserEmploymentSkillRepo,
)


class UserEmploymentController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_repo = UserRepo()
        self.user_employment_repo = UserEmploymentRepo()
        self.user_employment_skill_repo = UserEmploymentSkillRepo()
        self.skill_repo = SkillRepo()

    def _get_employment_skills(self, employment_id):
        skills_list = []
        skills = self.user_employment_skill_repo.get_unpaginated(
            user_employment_id=employment_id
        )
        for skill in skills:
            skill_data = self.skill_repo.find_first(id=skill)
            skill_dict = skill_data.serialize()
            skill_dict["name"] = skill_data.name
            skills_list.append(skill_dict)
        return skills_list

    def list_user_employment_history(self, user_id):
        user_employments = self.user_employment_repo.get_unpaginated(user_id=user_id)

        user_employment_list = []
        for user_employment in user_employments:
            user_employment_dict = user_employment.serialize()
            user_employment_dict["skills"] = self._get_employment_skills(
                user_employment.id
            )
            user_employment_list.append(user_employment_dict)
        return self.handle_response(
            "OK",
            payload={
                "user_employments": user_employment_list,
            },
        )

    def get_user_employment(self, user_employment_id):
        user_employment = self.user_employment_repo.get(user_employment_id)

        if user_employment:
            user_employment_dict = user_employment.serialize()
            user_employment_dict["skills"] = self._get_employment_skills(
                user_employment.id
            )
            return self.handle_response(
                "OK", payload={"user_employment": user_employment_dict}
            )
        return self.handle_response(
            "Invalid User Employment or Missing user_employment_id", status_code=400
        )

    def create_user_employment(self):
        (
            user_id,
            institution_name,
            job_title,
            employment_type,
            institution_url,
            institution_city,
            institution_country,
            institution_size,
            work_summary,
            accomplishments,
            start_date,
            end_date,
            is_current,
            skills,
        ) = self.request_params(
            "user_id",
            "institution_name",
            "job_title",
            "employment_type",
            "institution_url",
            "institution_city",
            "institution_country",
            "institution_size",
            "work_summary",
            "accomplishments",
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

            user_employment = self.user_employment_repo.new_user_employment(
                user_id=user_id,
                institution_name=institution_name,
                job_title=job_title,
                employment_type=employment_type,
                institution_url=institution_url,
                institution_city=institution_city,
                institution_country=institution_country,
                institution_size=institution_size,
                work_summary=work_summary,
                accomplishments=accomplishments,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
            )
            skills_dict = self._process_skills(user_employment.id, skills)

            user_employment_serialized = user_employment.serialize()
            user_employment_serialized["skills"] = skills_dict
            return self.handle_response(
                "OK",
                payload={"user_employment": user_employment_serialized},
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

    def _process_skills(self, user_employment_id, skills):
        skills_dict = []

        if skills is not None:

            for skill in skills:
                user_employment_skills = (
                    self.user_employment_skill_repo.new_user_employment_skill(
                        user_employment_id=user_employment_id, skill_id=skill
                    )
                )
                skill_data = self.skill_repo.find_first(id=skill)
                user_employment_skill_dict = user_employment_skills.serialize()
                user_employment_skill_dict["name"] = skill_data.name
                skills_dict.append(user_employment_skill_dict)
        return skills_dict

    def update_user_employment(self, update_id):
        (
            user_id,
            user_employment_id,
            institution_name,
            job_title,
            employment_type,
            institution_url,
            institution_city,
            institution_country,
            institution_size,
            work_summary,
            accomplishments,
            start_date,
            end_date,
            is_current,
            skills,
        ) = self.request_params(
            "user_id",
            "user_employment_id",
            "institution_name",
            "job_title",
            "employment_type",
            "institution_url",
            "institution_city",
            "institution_country",
            "institution_size",
            "work_summary",
            "accomplishments",
            "start_date",
            "end_date",
            "is_current",
            "skills",
        )
        if update_id != user_employment_id:
            return self.handle_response(
                "Invalid or incorrect user_employment_id provided", status_code=400
            )

        if skills is not None:
            self._validate_skills(skills)

        user_employment = self.user_employment_repo.get(user_employment_id)

        if not isinstance(start_date, datetime.date):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        if user_employment:
            updates = {
                "institution_name": institution_name,
                "job_title": job_title,
                "employment_type": employment_type,
                "institution_url": institution_url,
                "institution_city": institution_city,
                "institution_country": institution_country,
                "institution_size": institution_size,
                "work_summary": work_summary,
                "accomplishments": accomplishments,
                "start_date": start_date,
                "end_date": end_date,
                "is_current": is_current,
            }

            user_employment = self.user_employment_repo.update(
                user_employment, **updates
            )
            skills_dict = self._process_skills(user_employment.id, skills)
            user_employment_serialized = user_employment.serialize()
            user_employment_serialized["skills"] = skills_dict
            return self.handle_response(
                "OK",
                payload={"user_employment": user_employment_serialized},
            )

        return self.handle_response(
            "Invalid or incorrect user_employment_id provided", status_code=400
        )

    def delete_user_employment(self, user_employment_id):
        user_employment = self.user_employment_repo.get(user_employment_id)

        if user_employment:
            updates = {"is_deleted": True}
            self.user_employment_repo.update(user_employment, **updates)
            return self.handle_response(
                "user employment deleted", payload={"status": "success"}
            )
        return self.handle_response(
            "Invalid or incorrect user_employment_id provided", status_code=404
        )
