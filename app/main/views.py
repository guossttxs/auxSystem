#!/usr/bin/env python
#-*- coding:utf8 -*-

from flask import render_template, current_app
from . import main

@main.route('/', methods=['GET'])
def index():
    return 'hello world'
