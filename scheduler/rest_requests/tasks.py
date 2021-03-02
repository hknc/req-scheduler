from celery import current_app as task_app
from django.core.exceptions import ObjectDoesNotExist

from scheduler.rest_requests.models import RequestSchedule, Status
from scheduler.rest_requests.services import make_request


@task_app.task()
def process_request(request_schedule_id):
    """Processes a scheduled request."""

    try:
        schedule = RequestSchedule.objects.get(id=request_schedule_id)
    except ObjectDoesNotExist:
        return {"success": False, "error": {"message": "RequestScheduleDoesNotExist"}}

    response = make_request(
        schedule.rest_request.method,
        schedule.rest_request.url,
        schedule.rest_request.body,
        schedule.rest_request.headers,
    )

    if not response.get("ok", False):
        response = {
            "success": False,
            "error": {
                "code": response.get("status_code", "500"),
                "message": response.get("reason", "Server Error"),
            },
        }
        schedule.response_data = response
        schedule.status = Status.FAILED
        schedule.retry += 1
        schedule.save()
        return

    schedule.response_data = response.json()
    schedule.status = Status.PROCESSED
    schedule.save_related()

    return {"success": True}
