from flask import Flask

from routes.advent import advent
from routes.auth import auth

def create_app():
    app = Flask(__name__)
    app.register_blueprint(advent, url_prefix="/advent")
    app.register_blueprint(auth, url_prefix="/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
