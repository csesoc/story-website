from common.redis import cache
from database.database import clear_database


def clear_all():
    # Clear Redis
    cache.flushdb()

    # Clear database
    clear_database()
