from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth

url_prefix = '{}/skills'.format(BaseBlueprint.base_url_prefix)
skill_blueprint = Blueprint('skill', __name__, url_prefix=url_prefix)
	