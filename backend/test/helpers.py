from common.redis import cache
from database.database import clear_database
from database.user import add_user
from models.user import User


def db_add_user(email, username, password):
    add_user(email, username, User.hash_password(password), 0, 0)

def clear_all():
    # Clear Redis
    cache.flushdb()

    # Clear database
    clear_database()
