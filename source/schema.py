from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


def get_current_time():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str

class UserFile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    upload_date: datetime = Field(default_factory=get_current_time)\
    # Note file can exist without blob/ user for testing purposes. (REMOVE ONCE DONE)
    user_id: int | None = Field( default = None, foreign_key = "user.id")
    blob_id: int | None = Field( default = None, foreign_key = "fileblob.id")

class FileBlob(SQLModel,  table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(index=True)
    filepath: str = Field(index=True)
    size_in_bytes: int