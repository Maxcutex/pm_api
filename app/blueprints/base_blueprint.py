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

        self.app.register_blueprint(home_blueprint)
        self.app.register_blueprint(activity_blueprint)
        self.app.register_blueprint(role_blueprint)
        self.app.register_blueprint(user_blueprint)
