from rest_framework import serializers
from django.contrib.auth.models import User  # (not used yet, but fine)
from .models import (
    Driver,
    Trip,
    Feedback,
    DriverSentimentSummary,
    Alert,
    FeedbackConfig,
)


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ["id", "name", "employee_id"]


class DriverSentimentSummarySerializer(serializers.ModelSerializer):
    driver = DriverSerializer()

    class Meta:
        model = DriverSentimentSummary
        fields = ["driver", "avg_score", "total_feedback_count", "last_feedback_at"]


class AlertSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()

    class Meta:
        model = Alert
        fields = [
            "id",
            "driver",
            "avg_score_at_creation",
            "threshold",
            "status",
            "created_at",
        ]


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Custom serializer so that:
    - `driver` is sent as employee_id string (e.g. "DR008") from frontend
    - `trip` is sent as integer primary key
    We then resolve them to actual Driver/Trip objects in create().
    """

    # override fields: driver as string, trip as integer id
    driver = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    trip = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Feedback
        read_only_fields = ["sentiment_label", "sentiment_score", "created_at"]
        fields = [
            "id",
            "entity_type",
            "driver",      # employee_id string on input
            "trip",        # trip pk on input
            "rating",
            "text",
            "sentiment_label",
            "sentiment_score",
            "created_at",
        ]

    def create(self, validated_data):
        # pull out raw values
        driver_code = validated_data.pop("driver", None)
        trip_id = validated_data.pop("trip", None)

        driver_obj = None
        if driver_code:
            try:
                driver_obj = Driver.objects.get(employee_id=driver_code)
            except Driver.DoesNotExist:
                raise serializers.ValidationError(
                    {"driver": "Driver with this code does not exist."}
                )

        trip_obj = None
        if trip_id is not None:
            try:
                trip_obj = Trip.objects.get(pk=trip_id)
            except Trip.DoesNotExist:
                raise serializers.ValidationError(
                    {"trip": "Trip with this id does not exist."}
                )

        feedback = Feedback.objects.create(
            driver=driver_obj,
            trip=trip_obj,
            **validated_data,
        )
        return feedback


class FeedbackConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackConfig
        fields = ["key", "enabled"]
