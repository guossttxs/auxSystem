#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
from flask import Flask
from flask_cors import CORS
from config import config
from models.mongo import NXMongo

mongo = NXMongo()

def create_app():
    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV') if os.getenv('FLASK_ENV') else 'default'

    config_obj = config.get(config_name)
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    mongo.init_app(app.config['MONGO_URL'])

    from .main import main
    app.register_blueprint(main, url_prefix='/main')
    from .main import order
    app.register_blueprint(order, url_prefix='/order')

    if app.config.get('DEBUG'):
        CORS(app)

    return app
