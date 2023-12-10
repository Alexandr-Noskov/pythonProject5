import UrlValidator
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from main.models import Courses, Lesson

from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""
    class Meta:
        model = Lesson
        fields = '__all__'
        # Добавляем валидатор
        validators = [
            UrlValidator(fields=['lesson_name', 'lesson_description', 'video_url']),
            serializers.UniqueTogetherValidator(fields=['lesson_name', 'lesson_description'], queryset=Lesson.objects.all())
        ]


class LessonListSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков которые будут показываться при выводе КУРСОВ"""
    class Meta:
        model = Lesson
        fields = ['lesson_name', 'lesson_description']


# Для сериализатора модели курса реализуйте поле вывода уроков.

class CourseSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели курса """

    # Выводим счетчик уроков
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    # Расширяем сериализатор дополнительным вложенным полем с уроками
    lessons = serializers.SerializerMethodField()

    # Выводим имя пользователя в поле "owner", вместо цифры
    owner = SlugRelatedField(slug_field='first_name', queryset=User.objects.all())

    class Meta:
        model = Courses
        fields = '__all__'
        # Добавляем валидатор
        validators = [
            UrlValidator(fields=['name_courses', 'description_courses']),
            serializers.UniqueTogetherValidator(fields=['name_courses', 'description_courses'], queryset=Courses.objects.all())
        ]

    # Получаем все поля для дополнительного поля уроков с фильтрацией по курсу
    def get_lessons(self, course):
        return LessonListSerializer(Lesson.objects.filter(course=course), many=True).data