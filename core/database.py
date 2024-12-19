from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, joinedload
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

    def get_all_characters(self, character_name: str):
        # given a character name, lookup the main character and return all characters that are alts of that main character
        session = self.get_session()
        character = session.query(Character).filter(Character.name == character_name).first()
        # return all characters that have the same main_id as the character
        return session.query(Character).filter(Character.main_id == character.main_id).all()
    
    def get_top_characters_by_points(self, count: int):
        """Get the top N characters by their current points."""
        session = self.get_session()
        
        # return the top N characters by their current points
        # should only return main characters
        characters = session.query(Character).filter(Character.main_id == Character.id).order_by(desc(Character.current_with_twink)).limit(count).all()

        for character in characters:
            print(f"Character: {character.name}, Current Points: {character.current_with_twink}")

        return characters
        
      


