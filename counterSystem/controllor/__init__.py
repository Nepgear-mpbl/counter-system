from flask import Blueprint

controller = Blueprint('controller', __name__)
from . import admin, register, index, android
