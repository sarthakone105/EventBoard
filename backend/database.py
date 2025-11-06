import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Player, Judge, Event, Score  # ✅ fixed import

# Load .env only for local development
load_dotenv()

# Read environment variables (Render provides these automatically)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "tournament")

# Construct the connection URL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables automatically (only if not existing)
try:
    Base.metadata.create_all(bind=engine)
    print(f"✅ Connected to database: {DB_NAME} ({DB_HOST})")
except Exception as e:
    print("❌ Database connection failed:", e)
