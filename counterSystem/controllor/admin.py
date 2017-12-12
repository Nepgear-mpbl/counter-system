from flask import render_template
from ..model.models import Business, Counter, User
from . import controller
from flask import request, redirect, url_for
from .. import db
import json


@controller.route('/admin', methods=['GET'])
def admin_index():
    username = request.cookies.get('username')
    if username is None:
        return redirect(url_for('controller.index_index'))
    counter_id = request.cookies.get('counter')
    if counter_id is None:
        return redirect(url_for('controller.index_index'))
    business = Business.query.filter_by(valid=1, counter_id=counter_id).first()
    if business is None:
        working = False
    else:
        working = True
    return render_template('admin/index.html', username=username, working=working)


@controller.route('/admin/business/add', methods=['GET'])
def admin_add_business():
    user_id = request.args.get('user_id')
    business = Business(user_id=user_id, counter_id=None, valid=1)
    db.session.add(business)
    db.session.commit()
    res = json.dumps({'status': True, 'message': '叫号成功'}, ensure_ascii=False)
    return res


@controller.route('/admin/business/accept', methods=['POST'])
def admin_accept_business():
    username = request.cookies.get('username')
    if username is None:
        return json.dumps({'status': False, 'message': '请登录'}, ensure_ascii=False)
    counter_id = request.cookies.get('counter')
    if counter_id is None:
        return json.dumps({'status': False, 'message': '请登录'}, ensure_ascii=False)
    counter = Counter.query.filter_by(counter_id=counter_id).first()
    if counter is None:
        return json.dumps({'status': False, 'message': '数据库错误'}, ensure_ascii=False)
    all_business = Business.query.filter_by(valid=1, counter_id=None).all().order_by(Business.post_time)
    if all_business is None:
        return json.dumps({'status': False, 'message': '没有等待中的客户'}, ensure_ascii=False)
    all_business[0].counter_id = counter.counter_id
    db.session.commit()
    res = json.dumps({'status': True, 'message': '叫号成功'}, ensure_ascii=False)
    return res
