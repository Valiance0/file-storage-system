from functools import lru_cache
from typing import Iterator

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session
from source.models import  User, UserFile, FileBlob, UserSession

class DatabaseManager():
    engine: Engine
    models = [User, UserSession, UserFile, FileBlob]

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)

    def initialize_database(self):
        SQLModel.metadata.create_all(self.engine)

    def get_database(self) -> Iterator[Session] :
        with Session(self.engine) as session:
            yield session        

@lru_cache
def get_database_manager(database_url: str) -> DatabaseManager:
    return DatabaseManager(database_url)