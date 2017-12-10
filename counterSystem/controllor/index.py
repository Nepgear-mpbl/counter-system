from flask import render_template,request, make_response, redirect, url_for
from ..model.models import User, Counter
from . import controller
import json
import hashlib
from .. import db


@controller.route('/', methods=['GET'])
def index_index():
    username = request.cookies.get('username')
    if username is not None:
        return redirect(url_for('controller.admin_index'))
    counters = Counter.query.filter_by(user_id=None).all()
    return render_template('index/index.html', counters=counters,username=None)


@controller.route('/login', methods=['POST'])
def index_login():
    username = request.form['username']
    pwd = request.form['password']
    counter = request.form['counter']
    user = User.query.filter_by(username=username).first()
    if user == None:
        res = json.dumps({'status': False, 'message': '用户名或密码错误'}, ensure_ascii=False)
    else:
        salt = user.salt
        e_pwd = user.pwd
        md5 = hashlib.sha256()
        md5.update((pwd + salt).encode("utf8"))
        if md5.hexdigest() == e_pwd:
            counter = Counter.query.filter_by(counter_id=counter).first()
            counter.user_id = user.user_id
            db.session.commit()
            res = json.dumps({'status': True, 'message': '登陆成功'}, ensure_ascii=False)
            res = make_response(res)
            res.set_cookie('username', username)
        else:
            res = json.dumps({'status': False, 'message': '用户名或密码错误'}, ensure_ascii=False)
    return res


@controller.route('/logout', methods=['GET'])
def index_logout():
    username = request.cookies.get('username')
    user = User.query.filter_by(username=username).first()
    counter = Counter.query.filter_by(user_id=user.user_id).first()
    counter.user_id = None
    db.session.commit()
    res = redirect(url_for('controller.index_index'))
    res.delete_cookie('username')
    return res
