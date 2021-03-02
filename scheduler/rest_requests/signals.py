from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .apps import RestRequestsConfig
from .models import RequestSchedule, RestRequest


def create_default_permissions(sender, **kwargs):

    default_user_group, created = Group.objects.get_or_create(name="default_user_group")
    if default_user_group:
        # RequestSchedule permissions
        request_schedule_permissions = Permission.objects.filter(
            content_type__app_label="rest_requests",
            content_type__model="requestschedule",
        )
        default_user_group.permissions.add(*request_schedule_permissions)

        # RestRequest permissions
        rest_request_permissions = Permission.objects.filter(
            content_type__app_label="rest_requests",
            content_type__model="restrequest",
        )
        default_user_group.permissions.add(*rest_request_permissions)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_default_user_group(sender, instance, created, **kwargs):
    if created:
        default_user_group = Group.objects.get(name="default_user_group")
        instance.groups.add(default_user_group)
