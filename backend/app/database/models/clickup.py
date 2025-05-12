from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.database.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    avatar = Column(String)

    members = relationship("Member", back_populates="team", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="team", cascade="all, delete-orphan")


class Member(Base):
    __tablename__ = "members"

    id = Column(String, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    role = Column(Integer)
    role_key = Column(String)
    initials = Column(String)
    avatar = Column(String)
    team_id = Column(String, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="members")
    assigned_tasks = relationship("Task", back_populates="assignee", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    date_created = Column(BigInteger)  # ← CORRIGIDO AQUI
    date_updated = Column(BigInteger)
    due_date = Column(BigInteger, nullable=True)
    assignee_id = Column(String, ForeignKey("members.id"), nullable=True)
    team_id = Column(String, ForeignKey("teams.id"))
    score = Column(Integer, nullable=True)
    month_collected = Column(String, index=True)

    assignee = relationship("Member", back_populates="assigned_tasks")
    team = relationship("Team", back_populates="tasks")