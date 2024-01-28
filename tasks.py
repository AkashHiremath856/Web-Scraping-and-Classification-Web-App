from celery import Celery
from DataAnnotator import main

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

@app.task
def scrape_url(url, save_to_db):
    # Your scraping logic here
    result = main(url)

    # Save to DB if needed
    if save_to_db:
        # Your DB saving logic here
        pass

    return result
