import bcrypt
import persistence


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def get_password_hash_for_username(username):
    users = persistence.get_users()
    # returns the hashed password for that username
    try:
        return [user["password"] for user in users if user["username"] == username][0]
    except IndexError:
        return ''