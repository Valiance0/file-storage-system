from source.utils.config import get_settings
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()
DATABASE_URL: str = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in env variables.")

engine = create_engine(DATABASE_URL)

def get_database():
    with Session(engine) as session:
        yield session

class DatabaseManager():
