from flask_cors import cross_origin

from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Auth,
    Security,
)
from app.controllers.user_controller import UserController

# from flasgger import swag_from

user_blueprint = Blueprint(
    "user", __name__, url_prefix="{}/users".format(BaseBlueprint.base_url_prefix)
)
user_controller = UserController(request)


@user_blueprint.route("/admin", methods=["GET"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["create_user_roles"])
# @swag_from('documentation/get_all_admin_users.yml')
def list_admin_users():
    return user_controller.list_admin_users()


@user_blueprint.route("/", methods=["GET"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["view_users"])
# @swag_from('documentation/get_all_users.yml')
def list_all_users():
    return user_controller.list_all_users()


@user_blueprint.route("/<int:id>/", methods=["DELETE"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["delete_user"])
# @swag_from('documentation/delete_user.yml')
def delete_user(id):
    return user_controller.delete_user(id)


@user_blueprint.route("/", methods=["POST"])
@Auth.has_permission(["create_user"])
@Security.validator(
    [
        "role_id|required",
        "gender|required",
        "date_of_birth|required",
        "password|required",
        "first_name|required",
        "last_name|required",
        "userId|optional",
        "imageUrl|optional:url",
    ]
)
# @swag_from('documentation/create_user.yml')
def create_user():
    return user_controller.create_user()


@user_blueprint.route("/check_email_exists", methods=["GET"])
# @swag_from('documentation/create_user.yml')
def check_email():
    email = request.args.get("email")
    return user_controller.check_email(email)


@user_blueprint.route("/register/", methods=["POST"])
@Security.validator(
    [
        "role_id|required",
        "gender|required",
        "date_of_birth|required",
        "employment_date|required",
        "password|required",
        "first_name|required",
        "last_name|required",
        "userId|optional",
        "imageUrl|optional:url",
    ]
)
# @swag_from('documentation/create_user.yml')
def register():
    return user_controller.register()


@user_blueprint.route("/update/<int:id>", methods=["POST"])
@Security.validator(
    [
        "role_id|required",
        "gender|required",
        "date_of_birth|required",
        "employment_date|required",
        "password|optional",
        "first_name|required",
        "last_name|required",
        "userId|optional",
        "imageUrl|optional:url",
    ]
)
# @swag_from('documentation/create_user.yml')
def update():
    return user_controller.update()


@user_blueprint.route("/<int:id>/", methods=["GET"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["view_users", "view_users_self"])
# @swag_from('documentation/get_user.yml')
def list_user(id):
    return user_controller.list_user(id)


@user_blueprint.route("/<int:user_id>/summary", methods=["PUT", "PATCH"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["update_user", "update_user_self"])
# @swag_from('documentation/update_user.yml')
def update_user_summary(user_id):
    return user_controller.update_user_summary(user_id)


@user_blueprint.route("/<int:user_id>", methods=["PUT", "PATCH"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["update_user", "update_user_self"])
@Security.validator(
    [
        "role_id|required",
        "gender|required",
        "date_of_birth|required",
        "employment_date|required",
        "password|optional",
        "first_name|required",
        "last_name|required",
        "user_id|optional",
        "imageUrl|optional:url",
    ]
)
# @swag_from('documentation/update_user.yml')
def update_user(user_id):
    return user_controller.update_user(user_id)


@user_blueprint.route("/<int:user_id>/info", methods=["PUT", "PATCH"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["update_user", "update_user_self"])
@Security.validator(
    [
        "first_name|required",
        "last_name|required",
        "job_title|optional",
        "experience_years|optional",
        "phone|optional",
        "user_id|required",
        "git_hub|optional",
        "linked_in|optional",
        "personal_email|optional:email",
    ]
)
# @swag_from('documentation/update_user.yml')
def update_user_info(user_id):
    return user_controller.update_user_info(user_id)


@user_blueprint.route("/<int:user_id>/image", methods=["PUT", "PATCH"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["update_user", "update_user_self"])
@Security.validator(
    [
        "image_url|required",
    ]
)
def update_profile_image(user_id):
    return user_controller.update_profile_image(user_id)


@user_blueprint.route("/generate_presigned_url", methods=["GET"])
# @cross_origin(supports_credentials=True)
@Auth.has_permission(["update_user", "update_user_self"])
def generate_presigned_url(file_name, expiration):
    return user_controller.generate_presigned_url(file_name, expiration)


@user_blueprint.route("/login", methods=["POST"])
def authenticate_user():
    return user_controller.authenticate_user()
