from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_links

class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_links])

    class Meta:
        model = Lesson
        fields = ["id","title", "course","owner","video_url"]


class CourseSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()
    info_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_count_of_lessons(self, obj):
        return obj.lesson_set.count()

    def get_info_lessons(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if not user.is_authenticated:  # Если пользователь не авторизован
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "preview",
            "count_of_lessons",
            "info_lessons",
            "is_subscribed"
        )
