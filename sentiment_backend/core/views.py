from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import DriverSentimentSummary, Alert, FeedbackConfig
from .serializers import (
    FeedbackSerializer,
    DriverSentimentSummarySerializer,
    AlertSerializer,
    FeedbackConfigSerializer,
)


from .ml_sentiment import VaderSentimentEngine

engine = VaderSentimentEngine()

class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Save feedback (create() in serializer resolves driver=employee_id, trip=pk)
        feedback = serializer.save(user=self.request.user)

        # 2. Run sentiment engine on text
        label, score = engine.score(feedback.text)
        feedback.sentiment_label = label
        feedback.sentiment_score = score
        feedback.save()

        # 3. If it's driver feedback, update rolling average + alert
        if feedback.entity_type == "DRIVER" and feedback.driver:
            summary, _ = DriverSentimentSummary.objects.get_or_create(
                driver=feedback.driver
            )

            n = summary.total_feedback_count
            old_avg = summary.avg_score or 0.0

            # Use sentiment_score (1–5)
            new_avg = (old_avg * n + score) / (n + 1)

            summary.avg_score = new_avg
            summary.total_feedback_count = n + 1
            summary.last_feedback_at = timezone.now()
            summary.save()

            # Alert logic
            threshold = 2.5
            if new_avg < threshold:
                # Don't spam alerts: only one OPEN at a time
                open_exists = Alert.objects.filter(
                    driver=feedback.driver, status=Alert.STATUS_OPEN
                ).exists()
                if not open_exists:
                    Alert.objects.create(
                        driver=feedback.driver,
                        avg_score_at_creation=new_avg,
                        threshold=threshold,
                    )


class DriverSentimentListView(generics.ListAPIView):
    """
    Returns all DriverSentimentSummary rows so the admin dashboard can render them.
    """
    serializer_class = DriverSentimentSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DriverSentimentSummary.objects.select_related("driver").all()


class AlertListView(generics.ListAPIView):
    queryset = Alert.objects.select_related("driver").order_by("-created_at")
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def feedback_config_view(request):
    configs = FeedbackConfig.objects.all()
    serializer = FeedbackConfigSerializer(configs, many=True)
    return Response(serializer.data)
