
from flask import Flask
def create_app(config_object = 'cfg.settings'):
    app =  Flask(__name__)

    app.config.from_object(config_object)
    return app
    