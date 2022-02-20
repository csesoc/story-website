import os

from flask import Flask, json
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

from auth.user import User
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
    app.secret_key = os.environ["FLASK_SECRET"]

    app.register_blueprint(advent, url_prefix="/advent")
    app.register_blueprint(auth, url_prefix="/auth")

    app.register_error_handler(HTTPException, handle_exception)

    manager = LoginManager()
    manager.init_app(app)

    @manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
