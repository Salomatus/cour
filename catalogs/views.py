from django.views.generic import TemplateView
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Subscription
from .paginations import CustomPagination
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner



class HomePageView(TemplateView):
    template_name = "home.html"


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Привязка курса к авторизованному пользователю"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()


    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """Привязка урока к авторизованному пользователю"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=request.user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена."
        else:
            Subscription.objects.create(user=request.user, course=course)
            message = "Подписка добавлена."

        return Response({"message": message})
