from flask_cors import cross_origin

from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Security,
    Auth,
)
from app.controllers.user_project_controller import UserProjectController

url_prefix = "{}/user_project".format(BaseBlueprint.base_url_prefix)
user_project_blueprint = Blueprint("user_project", __name__, url_prefix=url_prefix)
user_project_controller = UserProjectController(request)


@user_project_blueprint.route("/user/<int:user_id>", methods=["GET"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["view_user_project"])
# @swag_from('documentation/get_all_user_project.yml')
def list_user_projects(user_id):
    return user_project_controller.list_user_projects(user_id)


@user_project_blueprint.route("/user-single/<int:user_project_id>", methods=["GET"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["view_user_project"])
# @swag_from('documentation/get_user_project_by_id.yml')
def get_user_project(user_project_id):
    return user_project_controller.get_user_project(user_project_id)


@user_project_blueprint.route("/", methods=["POST"])
# @cross_origin(supports_credentials=True)
@Security.validator(
    [
        "user_id|required:int",
        "project_name|required:string",
        "project_url|optional:string",
        "project_description|required:string",
        "start_date|required:date",
        "end_date|required:date",
        "is_current|required",
        "skills|optional:list_int",
    ]
)
@Auth.has_permission(["create_user_project"])
# @swag_from('documentation/create_user_project.yml')
def create_user_project():
    return user_project_controller.create_user_project()


@user_project_blueprint.route("/<int:update_id>", methods=["PUT", "PATCH"])
# @cross_origin(supports_credentials=True)
@Security.validator(
    [
        "user_id|required:int",
        "user_project_id|required:int",
        "project_name|required:string",
        "project_url|optional:string",
        "project_description|required:string",
        "start_date|required:date",
        "end_date|required:date",
        "is_current|required",
        "skills|optional:list_int",
    ]
)
@Auth.has_permission(["update_user_project"])
# @swag_from("documentation/update_user_project.yml")
def update_user_project(update_id):
    return user_project_controller.update_user_project(update_id)


@user_project_blueprint.route("/<int:user_project_id>", methods=["DELETE"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["delete_user_project"])
# @swag_from("documentation/delete_user_project.yml")
def delete_user_project(user_project_id):
    return user_project_controller.delete_user_project(user_project_id)
