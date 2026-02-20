from sqlmodel import Session, select
from source.models import UserSession


class UserSessionPersistence():
    def get_token_by_user_id(self, session: Session, user_id: int) -> UserSession | None:
        return session.exec(select(UserSession).where(UserSession.user_id == user_id)).first()
    
    def get_user_id_by_token(self, session: Session, token: str) -> UserSession | None:
        return session.exec(select(UserSession).where(UserSession.token == token)).first()
    
    def create_new_user_session(self, session: Session, user_session: UserSession) -> UserSession:
        try:
            session.add(user_session)
            session.commit()
            session.refresh(user_session)
        except Exception:
            session.rollback()
            raise
        return user_session