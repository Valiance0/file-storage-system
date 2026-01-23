from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select
from database import engine, get_database
from schema import File, User

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def get_page():
    return {"message": "Online"}

@app.get("/show_database")
def show_database(database: Session = Depends(get_database)):
    users = database.exec(select(User)).all()
    return {"message": "Database Connection Succesful", "user_count": len(users)}