from flask import render_template
from ..model.models import Business, Counter
from . import controller
from flask import request, redirect, url_for
from .. import db
import json
import datetime


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
    all_business = Business.query.filter_by(valid=1, counter_id=None).order_by(Business.post_time).all()
    if all_business is None:
        return json.dumps({'status': False, 'message': '没有等待中的客户'}, ensure_ascii=False)
    all_business[0].counter_id = counter.counter_id
    db.session.commit()
    res = json.dumps({'status': True, 'message': '叫号成功'}, ensure_ascii=False)
    return res


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@controller.route('/admin/business/get', methods=['GET'])
def admin_get_business():
    all_business = db.engine.execute(
        'select username,post_time from business JOIN user ON business.user_id=user.user_id WHERE valid=1')
    data = json.dumps([(dict(row.items())) for row in all_business], default=datetime_handler)
    res = json.dumps({'code': 0, 'count': len(json.loads(data)), 'msg': '', 'data': json.loads(data)},
                     ensure_ascii=False)
    return res


@controller.route('/admin/business/finish', methods=['POST'])
def admin_finish_business():
    counter_id = request.cookies.get('counter')
    if counter_id is None:
        return json.dumps({'status': False, 'message': '请登录'}, ensure_ascii=False)
    business = Business.query.filter_by(counter_id=counter_id).first()
    if business is None:
        return json.dumps({'status': False, 'message': '请不要重复结束'}, ensure_ascii=False)
    business.counter_id = None
    business.valid = 0
    db.session.commit()
    res = json.dumps({'status': True, 'message': '叫号结束'}, ensure_ascii=False)
    return res
