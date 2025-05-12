from sqlalchemy import Column, Integer, String
from app.database.models.base import Base

class ScoringRule(Base):
    __tablename__ = "scoring_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    points = Column(Integer)
