from celery import Celery
from DataAnnotator import main


app = Celery("tasks", broker="pyamqp://guest@localhost//", backend="rpc://")


@app.task
def scrape_url(url, save_to_db):
    try:
        result = main(url, save_to_db)
        return result
    except Exception as e:
        return {"status": "Error", "message": str(e)}
