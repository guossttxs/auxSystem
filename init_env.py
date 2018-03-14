#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import random
import string

def __create_nonce_str():
    """
    生成随机字符串,包含大小写字母和数字
    :return: 随机生成的15位字符串
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

cfgs = {
    'dev': {
        'FLASK_CONFIG': 'development',
        'SECRET_KEY': __create_nonce_str,
    },
    'release': {
        'FLASK_CONFIG': 'production',
        'SECRET_KEY': __create_nonce_str,
    }
}


if __name__ == '__main__':
    pass