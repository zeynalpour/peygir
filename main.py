#main.py
from app.core.task_processor import process_tasks, fail_expired_tasks

from fastapi import FastAPI
from app.core.scheduler import start_scheduler

from contextlib import asynccontextmanager
from app.web.routes import router as web_router
from app.api.routes import router as api_router

from app.database import init_db


#---------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(web_router)
app.include_router(api_router, prefix="/api") 

@app.get("/")
async def root():
    return {"message": "Peygir is running."}

#---------------------------------------------------
