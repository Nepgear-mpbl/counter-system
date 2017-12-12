from flask import Blueprint

controller = Blueprint('controller', __name__)
from . import admin_controller, register_controller, index_controller, android_controller
