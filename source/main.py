import os
import shutil
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from sqlmodel import SQLModel, Session, select
from database import engine, get_database
from schema import File as FileDB, User

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.post("/upload")
def upload_file(file: UploadFile, database:Session = Depends(get_database)):
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="Missing file name.") 
    
    file_path = f"../storage/{filename}"
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = os.path.getsize(file_path)

    new_file = FileDB(filename = filename, file_path = file_path, file_hash = "temp", size_in_bytes=file_size)

    database.add(new_file)
    database.commit()
    database.refresh(new_file)

    return {"status":"success", "file_id": new_file.id, "filename" : new_file.filename}


@app.get("/show_database")
def show_database(database: Session = Depends(get_database)):
    users = database.exec(select(User)).all()
    return {"message": "Database Connection Succesful", "user_count": len(users)}