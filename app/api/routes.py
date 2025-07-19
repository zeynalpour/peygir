# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db, crud
from config.settings import DEFAULT_EXTEND_DEADLINE_MINUTES

router = APIRouter()

@router.post("/tasks/{task_id}/status/{new_status}")
def change_status(task_id: str, new_status: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.update_task_status(db, task, new_status)
    return {"message": f"Status updated to '{new_status}'"}

@router.post("/tasks/{task_id}/extend")
def extend_deadline(
    task_id: str,
    minutes: int = Query(
        None, 
        description=f"New deadline in minutes (optional, Defualt= {DEFAULT_EXTEND_DEADLINE_MINUTES})"),
    db: Session = Depends(get_db)
):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_deadline = minutes if minutes is not None else DEFAULT_EXTEND_DEADLINE_MINUTES
    task.deadline_minutes = new_deadline
    db.commit()
    return {"message": f"Deadline extended to {new_deadline} minutes"}
