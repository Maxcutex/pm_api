from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Security,
    Auth,
)
from app.controllers.skill_category_controller import SkillCategoryController

url_prefix = "{}/skills_categories".format(BaseBlueprint.base_url_prefix)
skills_category_blueprint = Blueprint(
    "skills_category", __name__, url_prefix=url_prefix
)
skills_category_controller = SkillCategoryController(request)


@skills_category_blueprint.route("/", methods=["GET"])
@Auth.has_permission(["view_skills_categories"])
# @swag_from('documentation/get_all_skill_categories.yml')
def list_skill_categories():
    return skills_category_controller.list_skills_categories()


@skills_category_blueprint.route("/<int:skill_category_id>", methods=["GET"])
@Auth.has_permission(["view_skills_categories"])
# @swag_from('documentation/get_skill_category_by_id.yml')
def get_skill_category(skill_category_id):
    return skills_category_controller.get_skills_category(skill_category_id)


@skills_category_blueprint.route("/", methods=["POST"])
@Security.validator(["name|required"])
@Auth.has_permission(["create_skills_categories"])
# @swag_from('documentation/create_skill_category.yml')
def create_skill_category():
    return skills_category_controller.create_skills_category()


@skills_category_blueprint.route("/<int:skill_category_id>", methods=["PUT", "PATCH"])
@Auth.has_permission(["update_skills_categories"])
# @swag_from("documentation/update_skill_category.yml")
def update_skill_category(skill_category_id):
    return skills_category_controller.update_skills_category(skill_category_id)


@skills_category_blueprint.route("/<int:skill_category_id>", methods=["DELETE"])
@Auth.has_permission(["delete_skills_categories"])
# @swag_from("documentation/delete_skill_category.yml")
def delete_skill_category(skill_category_id):
    return skills_category_controller.delete_skills_category(skill_category_id)
