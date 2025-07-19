#app/database/crud.py

from sqlalchemy.orm import Session
from .models import Task
from datetime import datetime, timezone

def create_task(db: Session, task_id: str):
    '''
    درج با وضعیت در حال انجام
    '''
    task = Task(task_id=task_id, status="In Progress")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: str):
    '''
    دریافت تسک
    '''
    return db.query(Task).filter(Task.task_id == task_id).first()


def update_task_status(db: Session, task: Task, status: str):
    '''
    تغییر وضعیت تسک
    '''
    task.status = status
    db.commit()
    return task

def get_expired_tasks(db: Session):
    '''
    تسک‌های قدیمی رو پیدا میکنه
    '''
    now = datetime.now(timezone.utc)
    tasks = db.query(Task).filter(Task.status == "In Progress").all()

    expired = []
    for task in tasks:
        age = now - task.updated_at.replace(tzinfo=timezone.utc)
        if age.total_seconds() > task.deadline_minutes * 60:
            expired.append(task)

    return expired