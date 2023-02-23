from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import StudentModelViewSet, StudentSendEmailView

app_name = "student"

router = DefaultRouter()
router.register(r"Students", StudentModelViewSet, basename="student")

urlpatterns = [
    path("send-email/", StudentSendEmailView.as_view(), name="student-send-email")
]

urlpatterns += router.urls
