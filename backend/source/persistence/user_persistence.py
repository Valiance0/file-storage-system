from sqlmodel import Session, select
from typing import Sequence
from source.models import User


class UserPersistence:

    def get_user_by_name(self, session: Session, name: str) -> User | None:
        return session.exec(select(User).where(User.username == name)).first()
    
    def get_user_by_id(self, session: Session, id:int) -> User | None:
        return session.exec(select(User).where(User.id == id)).first()

    def get_all_users(self, session: Session) -> Sequence[User]:
        return session.exec(select(User)).all()

    def create_new_user(self, session: Session, user: User):
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
