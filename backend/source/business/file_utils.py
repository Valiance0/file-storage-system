
import os
import shutil
import uuid
from dotenv import load_dotenv
import hashlib
from fastapi import UploadFile

load_dotenv()

CHUNK_SIZE = 1048576 # 1MB

STORAGE_FILE_PATH: str = os.getenv("FILE_STORAGE_PATH", "")
if not STORAGE_FILE_PATH:
    raise ValueError("STORAGE_FILE_PATH not set in env variables.")



def process_file_upload(upload_file: UploadFile):
    hasher = hashlib.sha256()
    temp_path = f"{STORAGE_FILE_PATH}temp_{str(uuid.uuid4())}"
    file_size = 0

    with open(temp_path, "wb") as buffer:
        while True:
            chunk = upload_file.file.read(CHUNK_SIZE)
            if not chunk:
                break

            hasher.update(chunk)
            buffer.write(chunk)
            file_size += len(chunk)
    
    return {"hash": hasher.hexdigest(), "temp_path": temp_path, "size": file_size}

def save_file(temp_path: str, final_path: str):
    shutil.move(temp_path, final_path)

def delete_temp_file(temp_path: str):
    if os.path.exists(temp_path):
        os.remove(temp_path)