#app/web/routes.py

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.models import Task
from app.database import get_db

from fastapi import Form, status
from fastapi.responses import RedirectResponse

from zoneinfo import ZoneInfo
from datetime import timezone as dt_timezone


router = APIRouter()
templates = Jinja2Templates(directory="app/web/templates")

@router.get("/panel")
def task_panel(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.id).all()

    local_tz = ZoneInfo("Asia/Tehran")  
    for task in tasks:
        if task.updated_at.tzinfo is None:
            task.updated_at = task.updated_at.replace(tzinfo=dt_timezone.utc)
        task.updated_at = task.updated_at.astimezone(local_tz)

        if task.created_at.tzinfo is None:
            task.created_at = task.created_at.replace(tzinfo=dt_timezone.utc)
        task.created_at = task.created_at.astimezone(local_tz)

    return templates.TemplateResponse("panel.html", {"request": request, "tasks": tasks})

@router.post("/panel/extend/{task_id}")
def extend_deadline_form(task_id: str, minutes: int = Form(...), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.deadline_minutes += minutes
        db.commit()
    return RedirectResponse(url="/panel", status_code=status.HTTP_302_FOUND)

@router.post("/panel/status/{task_id}")
def change_status_form(
    task_id: str,
    new_status: str = Form(...),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.status = new_status
        db.commit()
    return RedirectResponse(url="/panel", status_code=status.HTTP_302_FOUND)