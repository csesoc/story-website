from common.redis import clear_redis
from database.database import clear_database
from database.user import add_user
from database.puzzle import add_part, add_question
from models.user import User

# def db_add_comp(compName, )
def db_add_question(name, dayNum, numParts):
    return add_question(name, dayNum, numParts)

def db_add_part(qid, partNum):
    add_part(qid, partNum)

def db_add_user(email, username, password):
    add_user(email, username, User.hash_password(password))

def clear_all():
    # Clear Redis
    clear_redis()

    # Clear database
    clear_database()
