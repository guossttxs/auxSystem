from datetime import datetime

from flask import render_template, current_app, request
from . import order
from .. import mongo
from utils.util import set_result, load_params
from utils.decorated import check_request_args

@order.route('modify_doctor', methods=['POST'])
@check_request_args(post=['order_sn', 'ptel', 'dtel'])
def ModifyOrderDoctor():
    values = load_params(request)
    ptel = values.get('ptel')
    dtel = values.get('dtel')
    order_sn = values.get('order_sn')
    order = mongo.db.order.find_one({'sn': order_sn})
    if not order:
        return set_result(1, '没有找到匹配的订单')
    
    patient = mongo.db.patient.find_one({'nxid': order.get('patient').get('nxid'), 'tel': ptel})
    doctor = mongo.db.doctor.find_one({'tel': dtel})
    following_doctors = [d.get('nxid') for d in patient.get('following')]
    if doctor.get('nxid') not in following_doctors:
        doctor_info = {
            'name': doctor.get('name'),
            'nxid': doctor.get('nxid'),
            'time': datetime.now(),
        }
        following = patient.get('following')
        following.append(doctor_info)
        mongo.db.patient.update({'nxid': patient.get('nxid')}, {
            '$set': {'following': following, 'attend': doctor_info}})
    order['info']['doctor']['nxid'] = doctor.get('nxid')
    order['info']['doctor']['name'] = doctor.get('name')
    mongo.db.order.save(order)

    return set_result(data={'order': order['nxid']})