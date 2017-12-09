from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .controllor import controller


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    print(config_name + ' mode on.')
    db.init_app(app)
    app.register_blueprint(controller)
    print('application initialized.')
    return app
