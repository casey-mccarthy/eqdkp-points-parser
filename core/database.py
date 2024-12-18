from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base, Character

class DatabaseManager:
    def __init__(self, db_name: str = "sqlite:///eqdkp_data.db"):
        self.engine = create_engine(db_name)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session() 
    
    def get_character_by_name(self, character_name: str):
        """Get a character by its name. This is case insensitive."""
        session = self.get_session()
        return session.query(Character).filter(Character.name.ilike(character_name)).first()
    
    def update_character_rank(self, character_name: str, rank_id: int, rank_name: str):
        session = self.get_session()
        character = session.query(Character).filter(Character.name == character_name).first()
        character.rank_id = rank_id
        character.rank_name = rank_name
        session.commit()