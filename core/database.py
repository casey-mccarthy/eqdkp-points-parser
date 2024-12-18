from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base

class DatabaseManager:
    def __init__(self, db_name: str = "sqlite:///eqdkp_data.db"):
        self.engine = create_engine(db_name)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session() 