from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .utils import schedule, revoke

User = get_user_model()

REQUEST_MAX_RETRY = 3


def get_default_schedule_datetime():
    # set default scheduled datetime at least one minute ahead
    return make_aware(datetime.now() + timedelta(minutes=1))


class Status(models.IntegerChoices):
    NOT_SET = 0, _("Not scheduled")
    PENDING = 1, _("Pending")
    PROCESSING = 2, _("Processing")
    PROCESSED = 3, _("Processed")
    FAILED = 4, _("Failed")
    CANCELLED = 5, _("Cancelled")


class RequestMethod(models.TextChoices):
    GET = "GET", _("GET")
    HEAD = "HEAD", _("HEAD")
    POST = "POST", _("POST")
    PUT = "PUT", _("PUT")
    DELETE = "DELETE", _("DELETE")
    OPTIONS = "OPTIONS", _("OPTIONS")
    PATCH = "PATCH", _("PATCH")


class HTTPSURLField(models.URLField):
    """URL field that accepts URLs that start with https:// only."""

    default_validators = [URLValidator(schemes=["https"])]


class RestRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_name = models.CharField(_("Request Name"), max_length=30, blank=True)
    url = HTTPSURLField(
        default="https://", max_length=200, help_text=_("Request URL, https:// only")
    )
    method = models.CharField(
        _("Method"),
        max_length=8,
        choices=RequestMethod.choices,
        default=RequestMethod.GET,
    )
    headers = models.JSONField(
        _("Request Headers"), default=dict, blank=True, null=True
    )
    body = models.JSONField(_("Request Body"), default=dict, blank=True, null=True)

    class Meta:
        verbose_name = _("Rest request")
        verbose_name_plural = _("Rest requests")

    def __str__(self):
        return f"{self.method} {str(self.url)} {self.request_name}"


class RequestSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rest_request = models.ForeignKey(RestRequest, on_delete=models.CASCADE)
    scheduled_date_time = models.DateTimeField(
        _("Scheduled Date Time"), default=get_default_schedule_datetime
    )
    status = models.IntegerField(
        _("Status"),
        choices=Status.choices,
        default=Status.NOT_SET,
    )
    task_id = models.CharField(blank=True, max_length=256)
    response_data = models.JSONField(_("Rest response"), blank=True, null=True)
    retry = models.IntegerField(
        _("Retry"),
        default=0,
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def schedule(self):
        if self.status in (Status.PROCESSED, Status.CANCELLED):
            return
        # set scheduled datetime at least one minute ahead
        default_schedule_datetime = get_default_schedule_datetime()
        now_30sec = timezone.localtime(timezone.now()) + timedelta(seconds=30)
        if self.scheduled_date_time.timestamp() < now_30sec.timestamp():
            self.scheduled_date_time = default_schedule_datetime

        task_id = schedule(self.id, self.scheduled_date_time)
        if task_id:
            if not self.task_id == "":
                revoke(self.task_id)
            self.task_id = task_id
            self.status = Status.PENDING
            self.save(skip_schedule=True)

    class Meta:
        verbose_name = _("Request schedule")
        verbose_name_plural = _("Request schedules")

    def __str__(self):
        return f"{str(timezone.localtime(self.scheduled_date_time))}"

    def save(self, *args, **kwargs):
        if kwargs.pop("skip_schedule", False):
            super().save(*args, **kwargs)
            return

        if self.retry > REQUEST_MAX_RETRY:
            self.status = Status.CANCELLED

        super().save(*args, **kwargs)
        # schedule for processing
        self.schedule()

    def save_related(self):
        self.rest_request.save()
        self.save()
