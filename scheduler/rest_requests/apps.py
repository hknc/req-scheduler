from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestRequestsConfig(AppConfig):
    name = "scheduler.rest_requests"
    verbose_name = _("Rest requests")
