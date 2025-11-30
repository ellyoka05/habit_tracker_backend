from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas
from models import HabitModel, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/habits", response_model=List[schemas.Habit])
def read_habits(
    x_user_id: str = Header(...), 
    db: Session = Depends(get_db)
):
    habits = db.query(HabitModel).filter(HabitModel.user_id == x_user_id).all()
    
    results = []
    for h in habits:
        habit_dict = h.__dict__
        habit_dict['completedDates'] = h.get_completed_dates()
        results.append(habit_dict)
    return results

@app.post("/api/habits", response_model=schemas.Habit)
def create_habit(
    habit: schemas.HabitCreate, 
    x_user_id: str = Header(...), 
    db: Session = Depends(get_db)
):
    db_habit = HabitModel(
        user_id=x_user_id, 
        name=habit.name,
        emoji=habit.emoji,
        colorValue=habit.colorValue,
        frequencyIndex=habit.frequencyIndex,
        startDate=habit.startDate,
        description=habit.description,
        goal=habit.goal,
        reminderHour=habit.reminderHour,
        reminderMinute=habit.reminderMinute
    )
    db_habit.set_completed_dates(habit.completedDates)
    
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    
    response = db_habit.__dict__
    response['completedDates'] = db_habit.get_completed_dates()
    return response

@app.put("/api/habits/{habit_id}", response_model=schemas.Habit)
def update_habit(
    habit_id: int, 
    habit: schemas.HabitCreate, 
    x_user_id: str = Header(...),
    db: Session = Depends(get_db)
):

    db_habit = db.query(HabitModel).filter(
        HabitModel.id == habit_id, 
        HabitModel.user_id == x_user_id
    ).first()
    
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found or access denied")
    
    db_habit.name = habit.name
    db_habit.emoji = habit.emoji
    db_habit.colorValue = habit.colorValue
    db_habit.frequencyIndex = habit.frequencyIndex
    db_habit.startDate = habit.startDate
    db_habit.description = habit.description
    db_habit.goal = habit.goal
    db_habit.reminderHour = habit.reminderHour
    db_habit.reminderMinute = habit.reminderMinute
    db_habit.set_completed_dates(habit.completedDates)
    
    db.commit()
    db.refresh(db_habit)
    
    response = db_habit.__dict__
    response['completedDates'] = db_habit.get_completed_dates()
    return response

@app.delete("/api/habits/{habit_id}")
def delete_habit(
    habit_id: int, 
    x_user_id: str = Header(...),
    db: Session = Depends(get_db)
):
    db_habit = db.query(HabitModel).filter(
        HabitModel.id == habit_id, 
        HabitModel.user_id == x_user_id
    ).first()
    
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found or access denied")
    
    db.delete(db_habit)
    db.commit()
    return {"ok": True}

# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000