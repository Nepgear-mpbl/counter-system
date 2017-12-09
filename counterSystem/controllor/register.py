from flask import render_template
from . import controller


@controller.route('/register', methods=['GET'])
def register_index():
    return render_template('register/index.html')