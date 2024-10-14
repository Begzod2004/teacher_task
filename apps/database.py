from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://TQQT:salom600@localhost:5432/tqqt"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Ma'lumotlar bazasini olish funksiyasi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
