from sanic import Sanic
from sanic_openapi import swagger_blueprint
from blueprints.config import decide_config


def create_app(environment=''):
    app = Sanic('metrobi')
    app.config.from_object(decide_config(environment))
    add_blueprints(app)
    return app


def add_blueprints(app):
    from .hello import hello_blueprint
    from .questions import questions_blueprint
    app.blueprint(swagger_blueprint)
    app.blueprint(hello_blueprint)
    app.blueprint(questions_blueprint)
