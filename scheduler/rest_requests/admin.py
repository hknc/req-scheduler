from django.contrib import admin
from django.contrib.auth import get_user_model

from scheduler.rest_requests.models import RequestSchedule, RestRequest

User = get_user_model()


@admin.register(RequestSchedule)
class RequestScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "rest_request",
        "scheduled_date_time",
        "status",
    )
    fields = (
        "rest_request",
        "scheduled_date_time",
        "status",
        "response_data",
        "retry",
    )
    readonly_fields = (
        "response_data",
        "retry",
    )
    list_filter = ("status", "rest_request__method")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not obj:
            form.base_fields["rest_request"].queryset = RestRequest.objects.filter(
                user=request.user
            )
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["rest_request", "response_data"]
        else:
            return ["response_data"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()


@admin.register(RestRequest)
class RestRequestAdmin(admin.ModelAdmin):
    fields = (
        "request_name",
        "url",
        "method",
        "headers",
        "body",
    )
    list_display = (
        "method",
        "url",
        "request_name",
    )
    list_filter = ("method",)

    def get_queryset(self, request):
        qs = super(RestRequestAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
