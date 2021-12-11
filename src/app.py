"""Main executor for monkey-do"""
from click import command, argument
from flask import Flask, request
from flask.wrappers import Response
import yaml

from entities import MonkeyResponse, MonkeySeeConfig
from utilities import routes_match

app = Flask('monkey_do_server')
mnkc_yaml = yaml.safe_load(open('config.mnkc').read())
MNKC: MonkeySeeConfig = MonkeySeeConfig(**mnkc_yaml)


@app.route('/')
def root():
    return 'monkey-do running'


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def mock_point(path: str) -> Response:
    """The proxy endpoint"""
    response = generate_response(path, request.method)
    return Response(response.body, status=response.status, mimetype='application/json')


def generate_response(route: str, method: str) -> MonkeyResponse:
    """TODO: docstring?"""
    # TODO: add a way to match parameterized routes
    # TODO: determine if method can be removed permanently
    
    handler_matches = list(filter(lambda handler: routes_match(handler.route, route), MNKC.handlers))

    if len(handler_matches) == 0:
        return MonkeyResponse(500, f'No handler found matching route: {route}')
    elif len(handler_matches) > 1:
        return MonkeyResponse(500, f'Found multiple matches for route: {route}')
    handler = handler_matches[0]

    # TODO: Add logic to deal with response scripts and external response.json files
    # For now just return the response object

    return handler.response

# TODO: Re-enable config loading once the config is no longer hard coded
# def load_config(file_name: str):
#     global MNKC
#     mnkc_yaml = yaml.safe_load(open(file_name).read())
#     MNKC = MonkeySeeConfig(**mnkc_yaml)

@command()
@argument('file')
def start_server(file):
    """TODO: docstring?"""
    # load_config(file)
    app.run(debug=True, port=MNKC.port)

if __name__ == '__main__':
    start_server()