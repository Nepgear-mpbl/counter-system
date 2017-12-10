from flask import render_template, redirect, url_for,request
from . import controller
import hashlib
import uuid
from ..model.models import User
import json
from .. import db


@controller.route('/register', methods=['GET'])
def register_index():
    username = request.cookies.get('username')
    if username is not None:
        return redirect(url_for('controller.admin_index'))
    return render_template('register/index.html',username=None)


@controller.route('/register', methods=['POST'])
def register_register():
    username = request.form['username']
    pwd = request.form['password']
    repeat_pwd = request.form['repeat-password']
    if pwd != repeat_pwd:
        res = json.dumps({'status': False, 'message': '两次输入的密码不一致'}, ensure_ascii=False)
        return res
    user = User.query.filter_by(username=username).first()
    if user is None:
        salt = str(uuid.uuid4()).replace('-', '')
        print(salt)
        md5 = hashlib.sha256()
        md5.update((pwd + salt).encode("utf8"))
        pwd = md5.hexdigest()
        data = User(username=username, salt=salt, pwd=pwd, type=1)
        db.session.add(data)
        db.session.commit()
        res = json.dumps({'status': True, 'message': '注册成功'}, ensure_ascii=False)
    else:
        res = json.dumps({'status': False, 'message': '用户名已存在'}, ensure_ascii=False)
    return res
