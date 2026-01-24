

import uuid
import bcrypt
from sqlmodel import Session, select

from schema import UserSession

def create_user_session(database: Session, user_id: int):
    token = str(uuid.uuid4())

    new_user_session = UserSession(token = token, user_id = user_id)
    database.add(new_user_session)
    database.commit()

    return token

def get_user_id(database: Session, token: str):
    
    database_session = database.exec(select(UserSession).where(UserSession.token == token)).first()
    if not database_session:
        return None
    
    return database_session.user_id

def create_password_hash(password: str):
    byte_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byte_password, salt)
    
def check_password(password: str, hash: str):
    byte_password = password.encode("utf-8")
    byte_hash = hash.encode("utf-8")
    return bcrypt.checkpw(byte_password, byte_hash)