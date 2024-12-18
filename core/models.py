from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from datetime import datetime
from typing import Optional

Base = declarative_base()

class CharacterPoints(Base):
    """Model for character DKP points information.
    
    This model is used to store the DKP points for a character.
    
    Attributes:
        id (int): The unique identifier for the character points.
        character_id (int): The ID of the character associated with these points.
        current (float): The current DKP points for the character.
        earned (float): The earned DKP points for the character.
        spent (float): The spent DKP points for the character.
        current_with_twink (float): The current DKP points with twink.
        earned_with_twink (float): The earned   DKP points with twink.
        spent_with_twink (float): The spent DKP points with twink.
        adjustment (float): The adjustment to the DKP points.
        adjustment_with_twink (float): The adjustment to the DKP points with twink.
    """
    __tablename__ = 'character_points'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    
    # Basic point values
    current = Column(Float, nullable=False, default=0.0)
    earned = Column(Float, nullable=False, default=0.0)
    spent = Column(Float, nullable=False, default=0.0)
    
    # Twink-related points
    current_with_twink = Column(Float, nullable=False, default=0.0)
    earned_with_twink = Column(Float, nullable=False, default=0.0)
    spent_with_twink = Column(Float, nullable=False, default=0.0)
    
    # Adjustments
    adjustment = Column(Float, nullable=False, default=0.0)
    adjustment_with_twink = Column(Float, nullable=False, default=0.0)
    
    # Relationship
    character = relationship("Character", back_populates="points")

class Character(Base):
    """Model for character information.
    
    This model is used to store the information for a character.
    
    Attributes:
        id (int): The unique identifier for the character.
        name (str): The name of the character.
        class_id (int): The ID of the class the character is.
        class_name (str): The name of the class the character is.
        active (bool): Whether the character is active.
        hidden (bool): Whether the character is hidden.
        main_id (int): The ID of the main character.
        main_name (str): The name of the main character.
        rank_id (int): The ID of the rank the character is.
        rank_name (str): The name of the rank the character is.
    """
    __tablename__ = 'characters'

    # Basic Information
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    class_id = Column(Integer, nullable=False)
    class_name = Column(String, nullable=False)

    # Rank Information can be empty for now
    rank_id = Column(Integer, nullable=True, default=None)
    rank_name = Column(String, nullable=True, default=None)
    
    # Status
    active = Column(Boolean, default=True)
    hidden = Column(Boolean, default=False)
    
    # Main/Alt Relationship
    main_id = Column(Integer, ForeignKey('characters.id'), nullable=True)
    main_name = Column(String, nullable=True)
    
    # Relationships
    points = relationship("CharacterPoints", back_populates="character", uselist=False)
    alts = relationship("Character", 
                        backref=backref("main", remote_side=[id]),
                        foreign_keys=[main_id])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



    def __repr__(self) -> str:
        return f"<Character(name='{self.name}', class_name='{self.class_name}', active={self.active})>" 