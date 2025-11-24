from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    FeedbackCreateView,
    DriverSentimentListView,
    AlertListView,
    feedback_config_view,
)

urlpatterns = [
    # auth
    path("auth/token/", obtain_auth_token, name="api_token_auth"),

    # feedback submit
    path("feedback/", FeedbackCreateView.as_view(), name="feedback-create"),

    # driver sentiment summaries for admin dashboard
    path(
        "drivers/sentiments/",
        DriverSentimentListView.as_view(),
        name="driver-sentiments",
    ),

    # alerts
    path("alerts/", AlertListView.as_view(), name="alerts"),

    # feature flags for feedback types
    path("config/feedback-types/", feedback_config_view, name="feedback-config"),
]
