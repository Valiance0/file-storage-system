from sqlmodel import Session, select
from typing import Sequence, Tuple
from source.models import FileBlob, UserFile


class FilePersistence():

    def get_file_by_id(self, session: Session, file_id: int) -> UserFile | None:
        statement = (
            select(UserFile)
            .where(UserFile.id == file_id)
        )
        
        return session.exec(statement).first()
    

    def get_file_by_name(self, session: Session, filename: str) -> UserFile | None:
        statement = (
            select(UserFile)
            .where(UserFile.filename == filename)
        )
        
        return session.exec(statement).first()

    def get_files_by_user_id(self, session: Session, user_id: int) -> Sequence[UserFile]:
        statement = (select(UserFile)
                     .where(UserFile.user_id == user_id)
        )

        return session.exec(statement).all()
    
    def get_blob_by_hash(self, session: Session, hash: str) -> FileBlob | None:
        return session.exec(select(FileBlob).where(FileBlob.hash == hash)).first()

    def create_file(self, session: Session, user_file: UserFile, file_blob: FileBlob):
        
        try:
            user_file.blob = file_blob
            session.add(user_file)
            session.commit()
            session.refresh(user_file)
        except Exception:
            session.rollback()
            raise
        
        return user_file
