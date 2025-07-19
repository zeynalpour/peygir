#app/core/task_processor.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
from app.database import crud
from config.settings import DATABASE_URL, THRESHOLD_MINUTES

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)



def process_tasks(task_ids):
    '''
    پردازش لیست وضایف دریافتی
    '''
    db = SessionLocal()
    try:
        for task_id in task_ids:
            task = crud.get_task(db, task_id)

            if not task:
                crud.create_task(db, task_id)
                print(f"Task {task_id} created.")
            elif task.status == "Failed":
                crud.update_task_status(db, task, "In Progress")
                print(f"Status of Task {task_id} changed to 'In Progress'.")
            else:
                print(f"Task {task_id} is already active. No change.")
    finally:
        db.close()


def fail_expired_tasks():
    '''
    تسک‌هایی که بیشتر از تایمر طول کشیدن رو به ناموفق تغییر وضعیت میده
    '''
    db = SessionLocal()
    try:
        stale_tasks = crud.get_expired_tasks(db)
        for task in stale_tasks:
            crud.update_task_status(db, task, "Failed")
            print(f"Task {task.task_id} FAILED.")
    finally:
        db.close()