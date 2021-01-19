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


@skill_blueprint.route('/')
def list_skills():
    return skill_controller.list_skills()


@skill_blueprint.route('/<int:id>/')
def get_skill(skill_id):
    return skill_controller.get_skill(skill_id)


def create_skill():
    pass


def update_skill(skill_id):
    pass


def delete_skill(skill_id):
    pass
