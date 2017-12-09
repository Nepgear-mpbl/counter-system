from flask import render_template
from ..model.models import User
from . import controller
from .. import db


@controller.route('/', methods=['GET'])
def index_index():
    # data=Tester(name="testuser",info="only for add test")
    # db.session.add(data)
    # db.session.commit()
    return render_template('index/index.html')
