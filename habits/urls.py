from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register(r"my_habits", HabitViewSet, basename="my_habits")

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="habits"),
] + router.urls
