from common.redis import clear_redis
from database.database import clear_database
from database.user import add_user
from models.user import User


def db_add_user(email, username, password):
    add_user(email, username, User.hash_password(password))

def clear_all():
    # Clear Redis
    clear_redis()

    # Clear database
    clear_database()

def get_cookie_from_header(response, cookie_name):
    cookie_headers = response.headers.getlist("Set-Cookie")

    for header in cookie_headers:
        attributes = header.split(";")

        if cookie_name in attributes[0]:
            cookie = {}

            for attr in attributes:
                split = attr.split("=")
                cookie[split[0].strip().lower()] = split[1] if len(split) > 1 else True

            return cookie

    return None

def generate_csrf_header(response):
    csrf_token = get_cookie_from_header(response, "csrf_access_token")["csrf_access_token"]
    return {"X-CSRF-TOKEN": csrf_token}
