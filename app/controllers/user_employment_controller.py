import datetime

from app.controllers.base_controller import BaseController
from app.repositories import UserRepo
from app.repositories.user_employment_repo import UserEmploymentRepo


class UserEmploymentController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_repo = UserRepo()
        self.user_employment_repo = UserEmploymentRepo()

    def list_user_employment_history(self, user_id):
        user_employments = self.user_employment_repo.get_unpaginated(user_id=user_id)

        user_employment_list = [
            user_employment.serialize() for user_employment in user_employments
        ]

        return self.handle_response(
            "OK",
            payload={
                "user_employments": user_employment_list,
            },
        )

    def get_user_employment(self, user_employment_id):
        user_employment = self.user_employment_repo.get(user_employment_id)
        if user_employment:
            return self.handle_response(
                "OK", payload={"user_employment": user_employment.serialize()}
            )
        return self.handle_response(
            "Invalid User Employment or Missing user_employment_id", status_code=400
        )

    def create_user_employment(self):
        (
            user_id,
            institution_name,
            job_title,
            start_date,
            end_date,
            is_current,
        ) = self.request_params(
            "user_id",
            "institution_name",
            "job_title",
            "start_date",
            "end_date",
            "is_current",
        )
        try:

            if not isinstance(start_date, datetime.date):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            if start_date > end_date:
                return self.handle_response(
                    "Start Date cannot be greater than End date ", status_code=400
                )
            user_employment = self.user_employment_repo.new_user_employment(
                user_id=user_id,
                institution_name=institution_name,
                job_title=job_title,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
            )
            return self.handle_response(
                "OK",
                payload={"user_employment": user_employment.serialize()},
                status_code=201,
            )
        except Exception as e:
            return self.handle_response("Error processing: " + str(e), status_code=400)

    def update_user_employment(self, update_id):
        (
            user_id,
            user_employment_id,
            institution_name,
            job_title,
            start_date,
            end_date,
            is_current,
        ) = self.request_params(
            "user_id",
            "user_employment_id",
            "institution_name",
            "job_title",
            "start_date",
            "end_date",
            "is_current",
        )
        if update_id != user_employment_id:
            return self.handle_response(
                "Invalid or incorrect user_employment_id provided", status_code=400
            )

        user_employment = self.user_employment_repo.get(user_employment_id)

        if not isinstance(start_date, datetime.date):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        if user_employment:
            updates = {
                "institution_name": institution_name,
                "job_title": job_title,
                "start_date": start_date,
                "end_date": end_date,
                "is_current": is_current,
            }

            self.user_employment_repo.update(user_employment, **updates)
            return self.handle_response(
                "OK", payload={"user_employment": user_employment.serialize()}
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
