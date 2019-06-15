import logging
import os

import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

ENV = os.environ["ENV"]
JOB_QUEUE_NAME = f"luigi-app-{ENV}"
JOB_DEFINITION_NAME = f"luigi-app-job-{ENV}"


def lambda_handler(event, _context):
    LOGGER.info(event)
    invoke_batch_job(event["DATE"])


def invoke_batch_job(target_date: str):
    client = boto3.client("batch")
    client.submit_job(
        jobDefinition=JOB_DEFINITION_NAME,
        jobQueue=JOB_QUEUE_NAME,
        jobName=f"luigi-app-{target_date}",
        parameters={"date": target_date},
    )
