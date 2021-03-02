import logging
from celery import current_app

from config.celery_app import app as task_app


def schedule(request_schedule_id, scheduled_date_time):
    """Schedules a request

    Parameters:
        request_schedule_id (int):
        scheduled_date_time (DateTime):

    Returns:
        task_id (uuid): Returns a uuid for the scheduled request

    """
    task_id = current_app.send_task(
        "scheduler.rest_requests.tasks.process_request",
        (request_schedule_id,),
        eta=scheduled_date_time,
    )
    return task_id


def revoke(task_id):
    """Revokes a scheduled task

    Parameters:
        task_id (uuid):
    """
    task_app.control.revoke(task_id)
