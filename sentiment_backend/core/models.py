from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"


class Trip(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="trips")
    trip_code = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.trip_code


class Feedback(models.Model):
    ENTITY_DRIVER = "DRIVER"
    ENTITY_TRIP = "TRIP"
    ENTITY_APP = "APP"
    ENTITY_MARSHAL = "MARSHAL"

    ENTITY_CHOICES = [
        (ENTITY_DRIVER, "Driver"),
        (ENTITY_TRIP, "Trip"),
        (ENTITY_APP, "Mobile App"),
        (ENTITY_MARSHAL, "Marshal"),
    ]

    SENTIMENT_POS = "POSITIVE"
    SENTIMENT_NEU = "NEUTRAL"
    SENTIMENT_NEG = "NEGATIVE"

    SENTIMENT_CHOICES = [
        (SENTIMENT_POS, "Positive"),
        (SENTIMENT_NEU, "Neutral"),
        (SENTIMENT_NEG, "Negative"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    entity_type = models.CharField(max_length=10, choices=ENTITY_CHOICES)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    trip = models.ForeignKey(Trip, null=True, blank=True, on_delete=models.SET_NULL)

    rating = models.IntegerField(null=True, blank=True)  # 1–5 optional
    text = models.TextField()

    sentiment_label = models.CharField(
        max_length=10, choices=SENTIMENT_CHOICES, null=True, blank=True
    )
    sentiment_score = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback #{self.id} ({self.entity_type})"


class DriverSentimentSummary(models.Model):
    driver = models.OneToOneField(
        Driver, on_delete=models.CASCADE, related_name="sentiment_summary"
    )
    avg_score = models.FloatField(default=0.0)
    total_feedback_count = models.IntegerField(default=0)
    last_feedback_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.driver} avg: {self.avg_score:.2f}"


class Alert(models.Model):
    STATUS_OPEN = "OPEN"
    STATUS_RESOLVED = "RESOLVED"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="alerts")
    avg_score_at_creation = models.FloatField()
    threshold = models.FloatField(default=2.5)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.driver} ({self.avg_score_at_creation})"


class FeedbackConfig(models.Model):
    """
    Feature flag for each feedback entity type.
    Example rows:
    - key = "driver", enabled=True
    - key = "trip", enabled=True
    - key = "app", enabled=False
    - key = "marshal", enabled=True
    """

    key = models.CharField(max_length=50, unique=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.key}: {self.enabled}"
