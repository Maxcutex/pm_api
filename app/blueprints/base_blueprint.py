from flask import Blueprint, request
from app.utils.security import Security
from app.utils.auth import Auth


class BaseBlueprint:

    base_url_prefix = "/api/v1"

    def __init__(self, app):
        self.app = app

    def register(self):

        """ Register All App Blue Prints Here """

        from app.blueprints.home_blueprint import home_blueprint
        from app.blueprints.user_blueprint import user_blueprint
        from app.blueprints.role_blueprint import role_blueprint
        from app.blueprints.activity_blueprint import activity_blueprint
        from app.blueprints.skills_category_blueprint import skills_category_blueprint
        from app.blueprints.user_employment_blueprint import user_employment_blueprint
        from app.blueprints.user_project_blueprint import user_project_blueprint
        from app.blueprints.skill_blueprint import skill_blueprint

        from app.blueprints.user_skill_blueprint import user_skill_blueprint
        from app.blueprints.user_education_blueprint import user_education_blueprint


        self.app.register_blueprint(home_blueprint)
        self.app.register_blueprint(activity_blueprint)
        self.app.register_blueprint(role_blueprint)
        self.app.register_blueprint(user_blueprint)
        self.app.register_blueprint(skills_category_blueprint)
        self.app.register_blueprint(user_employment_blueprint)
        self.app.register_blueprint(user_project_blueprint)
        self.app.register_blueprint(skill_blueprint)
        self.app.register_blueprint(user_skill_blueprint)
        self.app.register_blueprint(user_education_blueprint)
