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
