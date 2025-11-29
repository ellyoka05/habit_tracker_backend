from pydantic import BaseModel
from typing import List, Optional

class HabitBase(BaseModel):
    name: str
    emoji: str
    colorValue: int
    frequencyIndex: int
    startDate: str
    description: Optional[str] = None
    goal: Optional[int] = None
    reminderHour: Optional[int] = None
    reminderMinute: Optional[int] = None
    completedDates: List[str] = []

class HabitCreate(HabitBase):
    pass

class Habit(HabitBase):
    id: int

    class Config:
        from_attributes = True