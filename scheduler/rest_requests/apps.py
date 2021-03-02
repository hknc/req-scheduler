from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestRequestsConfig(AppConfig):
    name = "scheduler.rest_requests"
    verbose_name = _("Rest requests")

    def ready(self):
        from django.db.models.signals import post_migrate

        from .signals import add_default_user_group, create_default_permissions  # noqa

        post_migrate.connect(create_default_permissions, sender=self)
