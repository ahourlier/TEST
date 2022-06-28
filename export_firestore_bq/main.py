from venv import create

import uvicorn
from services import FirestoreUtils
from services import create_task
from services.thematiques import process_template
import os
import logging
from fastapi import FastAPI

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

app = FastAPI()

API_ROOT = "/api/firestore_export"

@app.get(f"{API_ROOT}")
async def root():
    return {"message": "Hello World"}


@app.get(f"{API_ROOT}/launch")
async def launch_task():
    create_task(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("QUEUES_LOCATION"),
        uri=f"{os.getenv('API_URL')}{API_ROOT}/task",
        method="POST",
        payload={}
    )
    return {"message": "All done"}

@app.post(f"{API_ROOT}/task")
async def run_export(payload: dict):
    """
    Export thematiques from Firestore in BQ for reporting
    @params: request: HTTP request from Cloud Functions
    """
    logging.info("Launching task")
    firestore_utils = FirestoreUtils()
    # fetch all templates
    templates = firestore_utils.list_templates()
    logging.info(f"fetched {len(templates)} templates")
    # for each template, process all entities with this template
    for idx, template in enumerate(templates):
        process_template(template, firestore_utils)
        logging.info(f"{idx + 1} done out of {len(templates)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)