from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime

Base = declarative_base()

class Character(Base):
    """Model for character information including DKP points."""
    
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
    
    # DKP Points
    current = Column(Float, nullable=False, default=0.0)
    earned = Column(Float, nullable=False, default=0.0)
    spent = Column(Float, nullable=False, default=0.0)
    current_with_twink = Column(Float, nullable=False, default=0.0)
    earned_with_twink = Column(Float, nullable=False, default=0.0)
    spent_with_twink = Column(Float, nullable=False, default=0.0)
    adjustment = Column(Float, nullable=False, default=0.0)
    adjustment_with_twink = Column(Float, nullable=False, default=0.0)
    
    # Relationships
    alts = relationship("Character", 
                        backref=backref("main", remote_side=[id]),
                        foreign_keys=[main_id])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Character(name='{self.name}', class_name='{self.class_name}', active={self.active})>" 