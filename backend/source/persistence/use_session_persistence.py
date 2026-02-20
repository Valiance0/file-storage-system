from sqlmodel import Session

from source.models import UserSession


class UserSessionPersistence():
    def get_token_by_user_id(self, session: Session, ) -> UserSession:
