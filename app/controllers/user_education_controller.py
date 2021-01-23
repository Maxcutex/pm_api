import datetime
from dateutil import relativedelta

from app.controllers.base_controller import BaseController
from app.repositories import (
    UserRepo,
    UserEducationRepo,
)
from app.utils.date_diff_functions import date_diff_string


class UserEducationController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_repo = UserRepo()
        self.user_education_repo = UserEducationRepo()

    def list_user_education(self, user_id):

        user_educations = self.user_education_repo.get_unpaginated(user_id=user_id)

        user_education_list = []

        for user_education in user_educations:
            user_education_dict = user_education.serialize()

            user_education_dict[
                "start_date_formatted"
            ] = user_education.start_date.strftime("%b, %Y")
            user_education_dict[
                "end_date_formatted"
            ] = user_education.end_date.strftime("%b, %Y")
            user_education_dict["duration"] = date_diff_string(
                user_education.start_date, user_education.end_date
            )
            user_education_dict["start_date"] = user_education.start_date.strftime(
                "%Y-%m-%d"
            )
            user_education_dict["end_date"] = user_education.end_date.strftime(
                "%Y-%m-%d"
            )

            user_education_list.append(user_education_dict)
        return self.handle_response(
            "OK",
            payload={
                "user_education": user_education_list,
            },
        )

    def get_user_education(self, user_education_id):
        user_education = self.user_education_repo.get(user_education_id)

        if user_education:
            user_education_dict = user_education.serialize()

            return self.handle_response(
                "OK", payload={"user_education": user_education_dict}
            )
        return self.handle_response(
            "Invalid User Education or Missing user_education_id", status_code=400
        )

    def create_user_education(self):
        (
            user_id,
            institution_name,
            course_name,
            degree_earned,
            accomplishments,
            institution_city,
            institution_country,
            start_date,
            end_date,
        ) = self.request_params(
            "user_id",
            "institution_name",
            "course_name",
            "degree_earned",
            "accomplishments",
            "institution_city",
            "institution_country",
            "start_date",
            "end_date",
        )
        try:

            if not isinstance(start_date, datetime.date):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            if start_date > end_date:
                return self.handle_response(
                    "Start Date cannot be greater than End date ", status_code=400
                )

            user_education = self.user_education_repo.new_user_education(
                user_id=user_id,
                institution_name=institution_name,
                course_name=course_name,
                degree_earned=degree_earned,
                accomplishments=accomplishments,
                institution_city=institution_city,
                institution_country=institution_country,
                start_date=start_date,
                end_date=end_date,
            )

            user_education_serialized = user_education.serialize()
            return self.handle_response(
                "OK",
                payload={"user_education": user_education_serialized},
                status_code=201,
            )
        except Exception as e:
            return self.handle_response("Error processing: " + str(e), status_code=400)

    def update_user_education(self, update_id):
        (
            user_id,
            user_education_id,
            institution_name,
            course_name,
            degree_earned,
            accomplishments,
            institution_city,
            institution_country,
            start_date,
            end_date,
        ) = self.request_params(
            "user_id",
            "user_education_id",
            "institution_name",
            "course_name",
            "degree_earned",
            "accomplishments",
            "institution_city",
            "institution_country",
            "start_date",
            "end_date",
        )
        if update_id != user_education_id:
            return self.handle_response(
                "Invalid or incorrect user_education_id provided", status_code=400
            )

        user_education = self.user_education_repo.get(user_education_id)

        if not isinstance(start_date, datetime.date):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        if user_education:
            updates = {
                "institution_name": institution_name,
                "course_name": course_name,
                "degree_earned": degree_earned,
                "accomplishments": accomplishments,
                "institution_city": institution_city,
                "institution_country": institution_country,
                "start_date": start_date,
                "end_date": end_date,
            }

            user_education = self.user_education_repo.update(user_education, **updates)
            user_education_serialized = user_education.serialize()
            return self.handle_response(
                "OK",
                payload={"user_education": user_education_serialized},
            )

        return self.handle_response(
            "Invalid or incorrect user_education_id provided", status_code=400
        )

    def delete_user_education(self, user_education_id):
        user_education = self.user_education_repo.get(user_education_id)

        if user_education:
            updates = {"is_deleted": True}
            self.user_education_repo.update(user_education, **updates)
            return self.handle_response(
                "user education deleted", payload={"status": "success"}
            )
        return self.handle_response(
            "Invalid or incorrect user_education_id provided", status_code=404
        )
