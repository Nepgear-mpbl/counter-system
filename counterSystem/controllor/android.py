from ..model.models import Business, Counter, User
from . import controller
from flask import request
from .. import db
import json


@controller.route('/android/business/add', methods=['GET'])
def android_add_business():
    user_id = request.args.get('user_id')
    business = Business(user_id=user_id, counter_id=None, valid=1)
    db.session.add(business)
    db.session.commit()
    res = json.dumps({'status': True, 'message': '叫号成功'}, ensure_ascii=False)
    return res


@controller.route('/android/business/info', methods=['GET'])
def android_info_business():
    user_id = request.args.get('user_id')
    # TODO 获取信息
    res = json.dumps({'status': True, 'message': '返回信息'}, ensure_ascii=False)
    return res
