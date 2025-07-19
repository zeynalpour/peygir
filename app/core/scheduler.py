#app/core/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.external_api import fetch_tasks
from app.core.task_processor import process_tasks, fail_expired_tasks
from config.settings import FETCH_INTERVAL_MINUTES
import logging

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s"
)

scheduler = BackgroundScheduler()

def fetch_and_process():
    logging.info("Running scheduled task cycle...")
    try:
        tasks = fetch_tasks()
        logging.info(f"Fetched tasks: {tasks}")
        process_tasks(tasks)
        fail_expired_tasks()
    except Exception as e:
        logging.error(f"Error in scheduled task: {e}")

scheduler.add_job(fetch_and_process, 'interval', minutes=FETCH_INTERVAL_MINUTES)

def start_scheduler():
    scheduler.start()
    logging.info("Scheduler started.")
