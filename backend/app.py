from werkzeug.exceptions import HTTPException
from flask import Flask, json

from routes.advent import advent
from routes.auth import auth

def handle_exception(error):
    response = error.get_response()

    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description
    })

    response.content_type = "application/json"

    return response

def create_app():
    app = Flask(__name__)

    app.register_blueprint(advent, url_prefix="/advent")
    app.register_blueprint(auth, url_prefix="/auth")

    app.register_error_handler(HTTPException, handle_exception)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
