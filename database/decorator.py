from .session import get_db_context
from functools import wraps

def use_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with get_db_context() as db:
            return func(*args, db=db, **kwargs)
    return wrapper