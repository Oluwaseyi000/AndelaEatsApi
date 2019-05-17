from flask_api import FlaskAPI
from flask_cors import CORS
from config import env, get_env
from app.utils import db #, timedelta
from app.blueprints.base_blueprint import BaseBlueprint
from app.utils.auth import Auth
from flasgger import Swagger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.utils.cron import Cron
import bugsnag
from bugsnag.flask import handle_exceptions

bugsnag.configure(
    api_key=get_env('BUGSNAG_API_KEY'),
    project_root=get_env('BUGSNAG_PROJECT_ROOT'),
)


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)
    app.config.from_object(env.app_env[config_name])
    app.config.from_pyfile('../config/env.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # CORS
    CORS(app)

    # Blueprints
    blueprint = BaseBlueprint(app)
    blueprint.register()

    # cron = Cron(app)
    # scheduler = BackgroundScheduler("Africa/Lagos")
    # # in your case you could change seconds to hours
    # scheduler.add_job(cron.run_24_hourly, trigger='interval', hours=24)
    # scheduler.add_job(cron.meal_session_cron)
    # scheduler.start()

    from . import models
    db.init_app(app)

    cron = Cron(app)
    scheduler = BackgroundScheduler(timezone="Africa/Lagos")
    # in your case you could change seconds to hours
    scheduler.add_job(cron.run_24_hourly, trigger='interval', hours=24)
    scheduler.add_job(cron.run_meal_session_cron, 'cron', day_of_week='mon-fri', hour=0, minute=0,
                      misfire_grace_time=None)
    scheduler.start()

    swg = Swagger(app)
    handle_exceptions(app)

    return app
