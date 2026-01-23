from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


def get_current_time():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str

class File(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    file_path: str = Field(index=True)
    file_hash: str = Field(index=True)
    size_in_bytes: int
    upload_date: datetime = Field(default_factory=get_current_time)
    user_id: int | None = Field( default = None, foreign_key = "user.id")
