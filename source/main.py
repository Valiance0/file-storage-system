import os
import shutil
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request, Response, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session, select, true

import file_utils
from database import engine, get_database
from schema import  User, UserFile, FileBlob
import auth


load_dotenv()
STORAGE_FILE_PATH: str = os.getenv("STORAGE_FILE_PATH", "")
if not STORAGE_FILE_PATH:
    raise ValueError("STORAGE_FILE_PATH not set in env variables.")


SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_or_create_file_blob(temp_path: str, hash : str, size_in_bytes: int, database:Session):
    database_blob = database.exec(select(FileBlob).where(FileBlob.hash == hash)).first()
    if database_blob:
        return database_blob
    else:
        final_file_name = hash
        final_path = f"{STORAGE_FILE_PATH}{final_file_name}"
        file_utils.save_file(temp_path, final_path)
        
        new_file_blob = FileBlob(hash=hash, filepath=final_path, size_in_bytes=size_in_bytes)
        database.add(new_file_blob)
        database.flush()
        database.refresh(new_file_blob)

        return new_file_blob

def create_user_file(filename: str, blob_id: int, user_id: int, database: Session):
    new_user_file = UserFile(user_id = user_id, filename=filename, blob_id = blob_id)
    database.add(new_user_file)
    database.flush()
    database.refresh(new_user_file)

    return new_user_file

@app.post("/register")
def register(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: Session = Depends(get_database)):
    username = form_data.username
    password = form_data.password

    existing_user = database.exec(select(User).where(User.username==username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username taken. Please pick a different one.")
    
    password_hash = auth.create_password_hash(password)
    
    new_user = User(username=username, password_hash=password_hash)
    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    if not new_user.id:
        raise HTTPException(status_code=400, detail="Database Failed to assign id for user.")

    token = auth.create_user_session(user_id=new_user.id, database=database)
    response.set_cookie(key="session_token", value=token, httponly=True, secure=True, samesite="strict")

    return {"status": "success", "username": username}

@app.post("/login")
def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: Session = Depends(get_database)):
    user = database.exec(select(User).where(User.username == form_data.username)).first()
    
    if not user or not auth.check_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect Username or Password.")

    if not user.id:
        raise ValueError(f"Database failed to create id for user{user.username}")

    token = auth.create_user_session(database = database, user_id = user.id)

    response.set_cookie(key="session_token", value=token, httponly=True, secure=True, samesite="strict")
    
    return {"status:": "success"}

@app.post("/upload")
def upload_file(upload_file: UploadFile, request: Request, database:Session = Depends(get_database)):
    token = request.cookies.get("session_token")
    current_user = auth.get_current_user(token = token or "", database = database)
    if not current_user.id:
        raise HTTPException(status_code=400, detail="User ID is missing")

    filename = upload_file.filename
    if not upload_file or not filename:
        raise HTTPException(status_code=400, detail="Missing file name.") 
    
    processed_upload = file_utils.process_file_upload(upload_file)
    hash = processed_upload["hash"]
    size_in_bytes = processed_upload["size"]
    temp_path = processed_upload["temp_path"]
    
    try:
        new_blob = get_or_create_file_blob(temp_path = temp_path, hash = hash, size_in_bytes=size_in_bytes, database=database) 
        
        if not new_blob.id:
            raise ValueError(f"Database failed to create blob_id for hash:{hash}")
        
        new_user_file = create_user_file(user_id = current_user.id,filename=filename, blob_id=new_blob.id, database=database)
        database.commit()
        return {"status":"success", "file_id": new_user_file.id, "filename" : new_user_file.filename}
    
    
    finally:
        file_utils.delete_temp_file(temp_path)


