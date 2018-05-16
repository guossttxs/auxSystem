#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""公用方法"""
import six
import requests
import json
import time
import string
from random import randint, choice
from datetime import datetime, date, timedelta


def post(url, data, headers=None):
    if headers is None:
        headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    # print(r.content)
    # print(r.headers)
    return r.content

def load_params(request):
    data = request.get_data()
    if data:
        return json.loads(data.decode())
    else:
        return {}

def set_result(code=0, msg='success', data={}):
    '''
    设置接口返回信息，JSON格式
    :param code: 0表示成功 1表示失败
    :param msg:  成功失败信息
    :param data: 返回的信息
    :return: JSON格式的结果信息
    '''
    return json.dumps({'code': code, 'msg': msg, 'data': data})

def get_datetime_formater(seperator='-', with_time=False, time_formater=None):
    formater = '%Y' + seperator + '%m' + seperator + '%d'
    if with_time:
        if time_formater is None:
            formater += ' %H:%M:%S'
        else:
            formater += ' '+time_formater
    return formater

def datetime2timestring(date_time, seperator='-', with_time=False):
    if not date_time:
        return ''
    if isinstance(date_time, datetime) or isinstance(date_time,date):
        formater = get_datetime_formater(seperator, with_time)
        return date_time.strftime(formater)
    return date_time

def timestring2datetime(timestring, seperator='-', with_time=False, time_formater=None):
    if not timestring:
        return ''
    formater = get_datetime_formater(seperator, with_time, time_formater)
    return datetime.strptime(timestring, formater)

def get_random_str():
    now = datetime.now()
    return now.strftime('%Y%m%d%H%M%S') + str(now.microsecond).zfill(6) + str(randint(0, 99)).zfill(2)

def get_cur_week_day(today=None):
    '''
    获取本周开始和结束日期
    :param today:
    :return:
    '''
    if today is None:
        today = datetime.now()
    today_week_num = datetime.weekday(today)
    cur_week_start = today - timedelta(today_week_num)
    cur_week_end = cur_week_start + timedelta(6)
    return datetime(cur_week_start.year, cur_week_start.month, cur_week_start.day, 0, 0, 0), \
        datetime(cur_week_end.year, cur_week_end.month, cur_week_end.day, 23, 59, 59)

def to_text(value, encoding='utf-8'):
    """将 value 转为 unicode，默认编码 utf-8

    :param value: 待转换的值
    :param encoding: 编码
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding='utf-8'):
    """将 values 转为 bytes，默认编码 utf-8

    :param value: 待转换的值
    :param encoding: 编码
    """
    if not value:
        return b''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)

    if six.PY3:
        return six.binary_type(str(value), encoding)  # For Python 3
    return six.binary_type(value)

def create_time_stamp(self):
    """
    生成时间戳
    :return:时间戳
    """
    return int(time.time())

def create_nonce_str():
    """
    生成随机字符串,包含大小写字母和数字
    :return: 随机生成的15位字符串
    """
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(15))

def create_out_trade_no():
    """
    生成订单号
    :return: 返回订单号
    """
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(randint(100000, 999999))
