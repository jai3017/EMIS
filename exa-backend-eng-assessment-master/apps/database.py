import urllib.parse
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

password = urllib.parse.quote("Apple@1234")
DATABASE_URL = "postgresql://admin:{}@localhost:5432/healthcare".format(password)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_data(db, db_patient):
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    db.close()


def get_session_local():
    yield SessionLocal()
