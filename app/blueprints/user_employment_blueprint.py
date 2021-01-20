from flask_cors import cross_origin

from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Security,
    Auth,
)
from app.controllers.user_employment_controller import UserEmploymentController

url_prefix = "{}/user_employment_history".format(BaseBlueprint.base_url_prefix)
user_employment_blueprint = Blueprint(
    "user_employment", __name__, url_prefix=url_prefix
)
user_employment_controller = UserEmploymentController(request)


@user_employment_blueprint.route("/user/<int:user_id>", methods=["GET"])
@cross_origin(supports_credentials=True)
@Auth.has_permission(["view_user_employment_history"])
# @swag_from('documentation/get_all_user_employment_history.yml')
def list_user_employment_history(user_id):
    return user_employment_controller.list_user_employment_history(user_id)


@user_employment_blueprint.route(
    "/user-single/<int:user_employment_id>", methods=["GET"]
)
@cross_origin(supports_credentials=True)
@Auth.has_permission(["view_user_employment_history"])
# @swag_from('documentation/get_user_employment_by_id.yml')
def get_user_employment(user_employment_id):
    return user_employment_controller.get_user_employment(user_employment_id)


@user_employment_blueprint.route("/", methods=["POST"])
@cross_origin(supports_credentials=True)
@Security.validator(
    [
        "user_id|required:int",
        "institution_name|required:string",
        "job_title|required:string",
        "start_date|required:date",
        "end_date|required:date",
        "is_current|required",
        "skills|optional:list_int",
    ]
)
@Auth.has_permission(["create_user_employment_history"])
# @swag_from('documentation/create_user_employment.yml')
def create_user_employment():
    return user_employment_controller.create_user_employment()


@user_employment_blueprint.route("/<int:update_id>", methods=["PUT", "PATCH"])
@cross_origin(supports_credentials=True)
@Security.validator(
    [
        "user_id|required:int",
        "user_employment_id|required:int",
        "institution_name|required:string",
        "job_title|required:string",
        "start_date|required:date",
        "end_date|required:date",
        "is_current|required",
        "skills|optional:list_int",
    ]
)
@Auth.has_permission(["update_user_employment_history"])
# @swag_from("documentation/update_user_employment.yml")
def update_user_employment(update_id):
    return user_employment_controller.update_user_employment(update_id)


@user_employment_blueprint.route("/<int:user_employment_id>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
@Auth.has_permission(["delete_user_employment_history"])
# @swag_from("documentation/delete_user_employment.yml")
def delete_user_employment(user_employment_id):
    return user_employment_controller.delete_user_employment(user_employment_id)
