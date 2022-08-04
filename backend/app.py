import os

from datetime import timedelta
from flask import Flask, json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from auth.jwt import update_token
from common.plugins import jwt, mail
from database.database import db
from routes.auth import auth
from routes.puzzle import puzzle
from routes.user import user


def handle_exception(error):
    response = error.get_response()

    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "message": error.description
    })

    response.content_type = "application/json"

    return response


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Add database
    app.config["DATABASE"] = db

    # Configure with all our custom settings
    app.config["JWT_SECRET_KEY"] = os.environ["FLASK_SECRET"]

    # TODO: set JWT_COOKIE_SECURE and JWT_COOKIE_SAMESITE to True on release
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["refresh"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    # TODO: convert to CSESoc SMTP server (if we have one) once we get that
    app.config["MAIL_SERVER"] = "smtp.mailtrap.io"
    app.config["MAIL_PORT"] = 2525
    app.config["MAIL_USERNAME"] = os.environ["MAILTRAP_USERNAME"]
    app.config["MAIL_PASSWORD"] = os.environ["MAILTRAP_PASSWORD"]
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False

    app.after_request(update_token)

    # Initialise plugins
    jwt.init_app(app)
    mail.init_app(app)

    # Register smaller parts of the API
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(puzzle, url_prefix="/puzzle")
    app.register_blueprint(user, url_prefix="/user")

    # Register our error handler
    app.register_error_handler(HTTPException, handle_exception)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001)
