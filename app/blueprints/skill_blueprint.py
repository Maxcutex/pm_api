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
skill_controller = SkilController(request)


def list_skills():
    pass


def get_skill(skill_id):
    pass

def create_skill():
    pass

def update_skill(skill_id):
    pass

def delete_skill(skill_id):
    pass
