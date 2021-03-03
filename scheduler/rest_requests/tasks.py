from celery import current_app as task_app
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist

from scheduler.rest_requests.models import RequestSchedule, Status
from scheduler.rest_requests.services import FailedRequestError, make_request

logger = get_task_logger(__name__)

REQUEST_RETRY_DELAY = 10


def get_response_data(response):
    if response is False:
        return {
            "status_code": 418,
            "reason": "request error",
        }

    response_data = {
        "status_code": response.status_code,
        "reason": response.reason,
        "body": response.json() if response else "",
        "elapsed": round(response.elapsed.total_seconds(), 2),
        "url": response.url,
    }
    return response_data


def set_schedule_failed(schedule, response=False):
    schedule.response_data = get_response_data(response)
    schedule.status = Status.PROCESSING
    schedule.retry += 1
    schedule.save()


@task_app.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=REQUEST_RETRY_DELAY,
    autoretry_for=(FailedRequestError,),
)
def process_request(self, request_schedule_id):
    """Processes a scheduled request."""

    try:
        schedule = RequestSchedule.objects.get(id=request_schedule_id)
    except ObjectDoesNotExist:
        raise

    try:
        response = make_request(
            schedule.rest_request.method,
            schedule.rest_request.url,
            schedule.rest_request.body,
            schedule.rest_request.headers,
        )

        if not response:
            set_schedule_failed(schedule, response)

    except FailedRequestError:
        # request failed
        set_schedule_failed(schedule)

    else:
        # successive request call
        schedule.response_data = get_response_data(response)
        schedule.status = Status.PROCESSED
        schedule.save_related()

        return {"status": "SUCCESS"}
