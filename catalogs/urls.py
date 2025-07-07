from django.urls import path
from rest_framework.routers import SimpleRouter

from catalogs.apps import CatalogsConfig
from catalogs.views import (CourseViewSet, HomePageView, LessonCreateApiView,
                       LessonDestroyApiView, LessonListApiView,
                       LessonRetrieveApiView, LessonUpdateApiView, SubscriptionAPIView)

app_name = CatalogsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
    path("subscribe/", SubscriptionAPIView.as_view(), name="subscribe"),
]

urlpatterns += router.urls