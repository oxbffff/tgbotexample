from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///main.db", echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
