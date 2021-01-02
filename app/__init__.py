from flask_api import FlaskAPI
from flask_cors import CORS
import bugsnag
import rollbar
import os
from config import env, get_env
from app.utils import db  # , timedelta
from app.blueprints.base_blueprint import BaseBlueprint
from apscheduler.schedulers.background import BackgroundScheduler

from app.utils.auth import Auth

bugsnag.configure(
    api_key=get_env("BUGSNAG_API_KEY"),
    project_root=get_env("BUGSNAG_PROJECT_ROOT"),
    notify_release_stages=["production", "staging"],
    release_stage=get_env("APP_ENV"),
)

rollbar.init(
    access_token=get_env("ROLLBAR_API_KEY"),
    environment=get_env("APP_ENV"),
    root=os.path.dirname(os.path.realpath(__file__)),
)


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)
    app.config.from_object(env.app_env[config_name])
    app.config.from_pyfile("../config/env.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # CORS
    CORS(app)

    # Blueprints
    blueprint = BaseBlueprint(app)
    blueprint.register()

    from . import models

    db.init_app(app)

    return app
