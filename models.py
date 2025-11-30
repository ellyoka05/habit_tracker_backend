from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./habits.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class HabitModel(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    # --- NEW COLUMN ---
    user_id = Column(String, index=True) # Stores "UserA", "UserB", or a UUID
    # ------------------
    name = Column(String, index=True)
    emoji = Column(String)
    colorValue = Column(Integer)
    frequencyIndex = Column(Integer)
    startDate = Column(String)
    description = Column(String, nullable=True)
    goal = Column(Integer, nullable=True)
    reminderHour = Column(Integer, nullable=True)
    reminderMinute = Column(Integer, nullable=True)
    
    completedDatesJson = Column(Text, default="[]")

    def get_completed_dates(self):
        return json.loads(self.completedDatesJson)

    def set_completed_dates(self, dates_list):
        self.completedDatesJson = json.dumps(dates_list)