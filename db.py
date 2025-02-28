from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv
import os
"""url = URL.create(
    drivername="postgresql",
    username="avnadmin",
    password="AVNS_w3wZO5vqRzgkJrdLQQV",
    host="pg-3d2ee583-steinnlabs-90b8.h.aivencloud.com",
    database="defaultdb",
    port=25995
)"""



load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL )

Session = sessionmaker(bind=engine)
session = Session()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    """_summary_
    try:
    # db.session.execute('SELECT 1')
    session.execute(text('SELECT 1'))
    print('\n\n----------- Connection successful !')
except Exception as e:
    print('\n\n----------- Connection failed ! ERROR : ', e)

    """


