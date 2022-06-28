import json
import logging
import os
import grpc
from uuid import uuid1

from google.api_core.exceptions import AlreadyExists
from google.api_core.retry import Retry
from google.cloud import tasks_v2
from google.cloud.tasks_v2.gapic.transports.cloud_tasks_grpc_transport import (
    CloudTasksGrpcTransport,
)


def create_task(
    project,
    location,
    uri,
    queue="firestore-export-queue",
    method="POST",
    payload=None,
    task_name=None,
    sync_id=None,
):
    oidc_token = {
        "service_account_email": "app-oslo-dev@appspot.gserviceaccount.com",
        "audience": "791703651725-7830vr66l8h6si8g9a2q04ln5hsjhigd.apps.googleusercontent.com",
    }
    task = {
        "http_request": {"http_method": method, "url": uri, "oidc_token": oidc_token}
    }
    if payload is not None:
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        task["http_request"]["body"] = payload.encode()

    if os.getenv("IS_LOCAL"):
        client = tasks_v2.CloudTasksClient(
            transport=CloudTasksGrpcTransport(
                channel=grpc.insecure_channel("127.0.0.1:9090"),
            )
        )
        queue_path = client.queue_path(project, location, queue)
        try:
            client.get_queue(queue_path)
        except:
            client.create_queue(
                client.location_path(project, location),
                {"name": queue_path},
                retry=Retry(initial=1, maximum=5),
            )

    else:
        client = tasks_v2.CloudTasksClient()

    if task_name is not None:
        logging.debug("Got task_name: %s", task_name)
        task["name"] = client.task_path(
            project, location, queue, "{}-{}".format(sync_id or uuid1(), task_name)
        )
        logging.debug("Generated task_path: %s", task["name"])

    try:
        return client.create_task(client.queue_path(project, location, queue), task)
    except AlreadyExists:
        logging.warning("The task {} already exists. Ignoring.".format(task["name"]))
        return None
    except Exception as e:
        logging.error(e)
