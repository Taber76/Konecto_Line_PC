from peewee import DoesNotExist
import bcrypt

from db.conection import DbConnection
from db.users.model import User


def authenticate(username, password):
    try:
        with DbConnection().db.connection_context():
            user = User.get(User.username == username)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True, user
            else:
                return False, None
    except DoesNotExist:
        print(f"User with username {username} does not exist.")
        return False, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None
