from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Security,
    Auth,
)
from app.controllers.skill_controller import SkillController

url_prefix = "{}/skills".format(BaseBlueprint.base_url_prefix)
skill_blueprint = Blueprint("skill", __name__, url_prefix=url_prefix)
skill_controller = SkillController(request)


@skill_blueprint.route("/", methods=["GET"])
@Auth.has_permission(["view_skill"])
def list_skills():
    return skill_controller.list_skills()


@skill_blueprint.route("/<int:id>/", methods=["GET"])
@Auth.has_permission(["view_skill"])
def get_skill(skill_id):
    return skill_controller.get_skill(skill_id)


@skill_blueprint.route("/", methods=["POST"])
@Security.validator(
    [
        "name|required:string",
        "skill_category_id|required:int",
    ]
)
@Auth.has_permission(["create_skill"])
def create_skill():
    return skill_controller.create_skill()


@skill_blueprint.route("/<int:skill_id>", methods=["PUT", "PATCH"])
@Security.validator(
    [
        "skill_id|required:int",
        "name|required:string",
        "skill_category_id|required:int",
    ]
)
@Auth.has_permission(["update_skill"])
def update_skill(skill_id):
    return skill_controller.update_skill(skill_id)


@skill_blueprint.route("/<int:skill_id>", methods=["DELETE"])
@Auth.has_permission(["delete_skill"])
def delete_skill(skill_id):
    return skill_controller.delete_skill(skill_id)
