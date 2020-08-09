from sanic.blueprints import Blueprint
from sanic.response import json
from sanic_openapi import doc

hello_blueprint = Blueprint('Hello', '/hello')


@doc.summary('Returns famous hello world json')
@hello_blueprint.route('/')
async def hello_root(request):
    return json({'hello': 'world'})
