from django.contrib import admin
from .models import (
    Driver,
    Trip,
    Feedback,
    DriverSentimentSummary,
    Alert,
    FeedbackConfig,
)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "employee_id")
    search_fields = ("name", "employee_id")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "trip_code", "driver", "started_at", "ended_at")
    search_fields = ("trip_code",)
    list_filter = ("driver",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "entity_type",
        "driver",
        "trip",
        "rating",
        "sentiment_label",
        "sentiment_score",
        "created_at",
    )
    list_filter = ("entity_type", "sentiment_label", "driver")
    search_fields = ("text",)


@admin.register(DriverSentimentSummary)
class DriverSentimentSummaryAdmin(admin.ModelAdmin):
    list_display = ("driver", "avg_score", "total_feedback_count", "last_feedback_at")
    search_fields = ("driver__name", "driver__employee_id")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("driver", "avg_score_at_creation", "threshold", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("driver__name", "driver__employee_id")


@admin.register(FeedbackConfig)
class FeedbackConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "enabled")
