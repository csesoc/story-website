import os

from datetime import timedelta
from flask import Flask, json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from auth.jwt import jwt, update_token
from routes.puzzle import puzzle
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
    cors = CORS(app)

    app.config["JWT_SECRET_KEY"] = os.environ["FLASK_SECRET"]

    # TODO: set JWT_COOKIE_SECURE and JWT_COOKIE_SAMESITE to True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["refresh"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_TOKEN_LOCATION"] = "cookies"

    app.after_request(update_token)

    jwt.init_app(app)

    app.register_blueprint(puzzle, url_prefix="/advent")
    app.register_blueprint(auth, url_prefix="/auth")

    app.register_error_handler(HTTPException, handle_exception)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001)
