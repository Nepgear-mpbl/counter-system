from flask import Blueprint

controller = Blueprint('controller', __name__)
from . import admin, update, index
