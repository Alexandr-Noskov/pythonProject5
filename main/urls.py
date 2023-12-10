from main.apps import MainConfig
from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import CoursesViewSet, LessonCreateAPIView


app_name = MainConfig.name
# роуетр для вьюсета ViewSet
router = DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='courses')
router.register(r'subscription', basename='subscription')

# Паттерны для Generic уроков Lessons
urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),

] + router.urls