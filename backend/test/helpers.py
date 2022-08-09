from common.redis import cache
from database.database import clear_database
from database.user import add_user
from models.user import User

def get_cookie_from_response(response, cookie_name):
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

def db_add_user(email, username, password):
    add_user(email, username, User.hash_password(password))

def clear_all():
    # Clear Redis
    cache.flushdb()

    # Clear database
    clear_database()
