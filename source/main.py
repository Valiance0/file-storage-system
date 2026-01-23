import os
import shutil
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from sqlmodel import SQLModel, Session, select

import file_utils
from database import engine, get_database
from schema import  User, UserFile, FileBlob


load_dotenv()
STORAGE_FILE_PATH: str = os.getenv("STORAGE_FILE_PATH", "")
if not STORAGE_FILE_PATH:
    raise ValueError("STORAGE_FILE_PATH not set in env variables.")


SQLModel.metadata.create_all(engine)

app = FastAPI()

# Still have to add user logic
@app.post("/upload")
def upload_file(upload_file: UploadFile, database:Session = Depends(get_database)):
    filename = upload_file.filename
    if not upload_file or not filename:
        raise HTTPException(status_code=400, detail="Missing file name.") 
    
    processed_upload = file_utils.process_file_upload(upload_file)
    hash = processed_upload["hash"]
    size_in_bytes = processed_upload["size"]
    temp_path = processed_upload["temp_path"]
    

    database_blob = database.exec(select(FileBlob).where(FileBlob.hash == hash)).first()

    if database_blob:
        file_utils.delete_temp_file(temp_path)
        final_blob_id = database_blob.id
        print(f"Duplicate blob uploaded, id:{final_blob_id}")
        status_message = "Uploaded (Duplicate Blob)"
    else:
        final_file_name = hash
        final_path = f"{STORAGE_FILE_PATH}{final_file_name}"
        file_utils.save_file(temp_path, final_path)
        
        new_file_blob = FileBlob(hash=hash, filepath=final_path, size_in_bytes=size_in_bytes)
        database.add(new_file_blob)
        database.commit()
        database.refresh(new_file_blob)

        final_blob_id = new_file_blob.id
        status_message = "Uploaded"

    new_user_file = UserFile(filename=filename, blob_id = final_blob_id)
    database.add(new_user_file)
    database.commit()
    database.refresh(new_user_file)

    return {"status":"success", "file_id": new_user_file.id, "filename" : new_user_file.filename}


@app.get("/show_database")
def show_database(database: Session = Depends(get_database)):
    users = database.exec(select(User)).all()
    return {"message": "Database Connection Succesful", "user_count": len(users)}