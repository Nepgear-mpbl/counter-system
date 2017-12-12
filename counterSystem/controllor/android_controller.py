from ..model.models import Business, User
from . import controller
from flask import request
from .. import db
import json
import hashlib
import uuid


@controller.route('/android/business/add', methods=['POST'])
def android_add_business():
    user_id = request.args.get('user_id')
    if user_id is None:
        return json.dumps({'status': False, 'message': '用户不存在'}, ensure_ascii=False)
    if User.query.filter_by(user_id=user_id).first() is None:
        return json.dumps({'status': False, 'message': '用户不存在'}, ensure_ascii=False)
    business = Business(user_id=user_id, counter_id=None, valid=1)
    db.session.add(business)
    db.session.commit()
    res = json.dumps({'status': True, 'message': '叫号成功'}, ensure_ascii=False)
    return res


@controller.route('/android/business/info', methods=['GET'])
def android_info_business():
    user_id = request.args.get('user_id')
    if user_id is None:
        return json.dumps({'status': False, 'message': '用户不存在'}, ensure_ascii=False)
    business = Business.query.filter_by(user_id=user_id).first()
    if business is None:
        return json.dumps({'status': False, 'message': '已不在队列中'}, ensure_ascii=False)
    post_time = business.post_time
    before_list = Business.query.filter_by(valid=1).filter(Business.post_time < post_time).all()
    if before_list is None:
        num = 0
    else:
        num = len(before_list)
    res = json.dumps({'status': True, 'num': num}, ensure_ascii=False)
    return res


@controller.route('/android/login', methods=['POST'])
def android_login():
    username = request.args.get('username')
    pwd = request.args.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None:
        res = json.dumps({'status': False, 'message': '用户名或密码错误'}, ensure_ascii=False)
    else:
        salt = user.salt
        e_pwd = user.pwd
        md5 = hashlib.sha256()
        md5.update((pwd + salt).encode("utf8"))
        if md5.hexdigest() == e_pwd:
            res = json.dumps({'status': True, 'message': '登陆成功'}, ensure_ascii=False)
        else:
            res = json.dumps({'status': False, 'message': '用户名或密码错误'}, ensure_ascii=False)
    return res


@controller.route('/android/register', methods=['POST'])
def android_register():
    username = request.args.get('username')
    pwd = request.args.get('password')
    repeat_pwd = request.args.get('repeat-password')
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
        data = User(username=username, salt=salt, pwd=pwd, type=0)
        db.session.add(data)
        db.session.commit()
        res = json.dumps({'status': True, 'message': '注册成功'}, ensure_ascii=False)
    else:
        res = json.dumps({'status': False, 'message': '用户名已存在'}, ensure_ascii=False)
    return res