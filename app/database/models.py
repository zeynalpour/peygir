#app/database/models.py

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from config.settings import DEFAULT_DEADLINE_MINUTES

Base = declarative_base()

class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key = True, autoincrement = True)
    task_id = Column(String, unique= True, index= True)
    status = Column(String, default="In Progress")     
    created_at = Column(DateTime(timezone=True), server_default=func.now())  
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 
    deadline_minutes = Column(Integer, default=DEFAULT_DEADLINE_MINUTES)

