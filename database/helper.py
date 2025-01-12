from config import settings
from database import MSSQLDatabase


def init_db_instance():
    return MSSQLDatabase()
