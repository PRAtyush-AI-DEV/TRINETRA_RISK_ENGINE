import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. .env file se password aur link load karo
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Engine: Ye database se baat karne wala main engine (truck) hai
engine = create_engine(DATABASE_URL)

# 3. SessionLocal: Har request par khulne wali pipe
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base: Ye humari aage aane wali tables ka blueprint banega
Base = declarative_base()

# Database connect karne ka helper function
def get_db():
    db = SessionLocal()
    try:
        yield db           #yield db: Yeh pipe FastAPI ko de do taaki wo data save kar sake. (yield ka matlab hai "ye lo apna tool aur kaam karo").
    finally:
        db.close()

print("✅ TRINETRA DATABASE ENGINE: READY")


# database/db_setup.py (The Transport Truck): Ye wo truck (Engine) hai jo tera data factory (Neon Cloud) tak lekar jayega aur wahan se layega.