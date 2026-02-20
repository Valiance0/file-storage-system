from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime, timezone


def get_current_time():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str

    sessions: list["UserSession"] = Relationship(back_populates="user")
    files: list["UserFile"] = Relationship(back_populates="user")

class UserSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token: str = Field(index=True)
    user_id: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="sessions")


class UserFile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    upload_date: datetime = Field(default_factory=get_current_time)

    user_id: int = Field(foreign_key = "user.id")
    blob_id: int = Field(foreign_key = "fileblob.id")

    user: "User" = Relationship(back_populates="files")
    blob: "FileBlob" = Relationship(back_populates="user_files")

class FileBlob(SQLModel,  table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(index=True)
    filepath: str = Field(index=True)
    size_in_bytes: int

    user_files: list["UserFile"] = Relationship(back_populates="blob")