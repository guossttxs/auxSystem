#!/usr/bin/env python
#-*- coding:utf8 -*-

from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main
    app.register_blueprint(main, url_prefix='/main')

    return app
