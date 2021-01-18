from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Security,
    Auth,
)
from app.controllers.user_skill_controller import UserSkillController

url_prefix = "{}/user_skill".format(BaseBlueprint.base_url_prefix)
user_skill_blueprint = Blueprint("user_skill", __name__, url_prefix=url_prefix)
user_skill_controller = UserSkillController(request)


@user_skill_blueprint.route("/user/<int:user_id>", methods=["GET"])
@Auth.has_permission(["view_user_skill"])
# @swag_from('documentation/get_all_user_skill.yml')
def list_user_skills(user_id):
    return user_skill_controller.list_user_skills(user_id)


@user_skill_blueprint.route("/user-single/<int:user_skill_id>", methods=["GET"])
@Auth.has_permission(["view_user_skill"])
# @swag_from('documentation/get_user_skill_by_id.yml')
def get_user_skill(user_skill_id):
    return user_skill_controller.get_user_skill(user_skill_id)


@user_skill_blueprint.route("/", methods=["POST"])
@Security.validator(
    [
        "user_id|required:int",
        "skill_level|required:string",
        "years|required:int",
        "skill_id|required:int",
    ]
)
@Auth.has_permission(["create_user_skill"])
# @swag_from('documentation/create_user_skill.yml')
def create_user_skill():
    return user_skill_controller.create_user_skill()


@user_skill_blueprint.route("/<int:user_skill_id>", methods=["PUT", "PATCH"])
@Security.validator(
    [
        "user_id|required:int",
        "skill_level|required:string",
        "years|required:int",
        "skill_id|required:int",
    ]
)
# @Auth.has_permission(["update_user_skill"])
# @swag_from("documentation/update_user_skill.yml")
def update_user_skill(user_skill_id):
    return user_skill_controller.update_user_skill(user_skill_id)


@user_skill_blueprint.route("/<int:user_skill_id>", methods=["DELETE"])
@Auth.has_permission(["delete_user_skill"])
# @swag_from("documentation/delete_user_skill.yml")
def delete_user_skill(user_skill_id):
    return user_skill_controller.delete_user_skill(user_skill_id)
