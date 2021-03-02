from django.contrib import admin
from scheduler.rest_requests.models import RestRequest, RequestSchedule


@admin.register(RequestSchedule)
class RequestScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(RestRequest)
class RestRequestAdmin(admin.ModelAdmin):
    pass
