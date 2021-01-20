from flask_cors import cross_origin

from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Security,
    Auth,
)
from app.controllers.user_education_controller import UserEducationController

url_prefix = "{}/user_education".format(BaseBlueprint.base_url_prefix)
user_education_blueprint = Blueprint("user_education", __name__, url_prefix=url_prefix)
user_education_controller = UserEducationController(request)


@user_education_blueprint.route("/user/<int:user_id>", methods=["GET"])
@cross_origin(supports_credentials=True)
@Auth.has_permission(["view_user_education"])
# @swag_from('documentation/get_all_user_education.yml')
def list_user_education(user_id):
    return user_education_controller.list_user_education(user_id)


@user_education_blueprint.route("/user-single/<int:user_education_id>", methods=["GET"])
@cross_origin(supports_credentials=True)
@Auth.has_permission(["view_user_education"])
# @swag_from('documentation/get_user_education_by_id.yml')
def get_user_education(user_education_id):
    return user_education_controller.get_user_education(user_education_id)


@user_education_blueprint.route("/", methods=["POST"])
@cross_origin(supports_credentials=True)
@Security.validator(
    [
        "user_id|required:int",
        "institution_name|required:string",
        "course_name|required:string",
        "degree_earned|required:string",
        "accomplishments|optional:string",
        "start_date|required:date",
        "end_date|required:date",
    ]
)
@Auth.has_permission(["create_user_education"])
# @swag_from('documentation/create_user_education.yml')
def create_user_education():
    return user_education_controller.create_user_education()


@user_education_blueprint.route("/<int:update_id>", methods=["PUT", "PATCH"])
@cross_origin(supports_credentials=True)
@Security.validator(
    [
        "user_id|required:int",
        "user_education_id|required:int",
        "institution_name|required:string",
        "course_name|required:string",
        "degree_earned|required:string",
        "accomplishments|optional:string",
        "start_date|required:date",
        "end_date|required:date",
    ]
)
@Auth.has_permission(["update_user_education"])
# @swag_from("documentation/update_user_education.yml")
def update_user_education(update_id):
    return user_education_controller.update_user_education(update_id)


@user_education_blueprint.route("/<int:user_education_id>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
@Auth.has_permission(["delete_user_education"])
# @swag_from("documentation/delete_user_education.yml")
def delete_user_education(user_education_id):
    return user_education_controller.delete_user_education(user_education_id)
