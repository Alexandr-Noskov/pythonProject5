from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from main.models import Courses
from main.paginators import EducationPaginator
from main.permissions import IsModeratorOrReadOnly, IsCourseOwner, IsPaymentOwner, IsCourseOrLessonOwner
from main.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
from users.models import UserRoles



class CoursesViewSet(viewsets.ModelViewSet):
    """Сериализатор для курсов"""
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOwner]
    pagination_class = EducationPaginator  # Пагинация

    class Meta:
        model = Courses
        fields = '__all__'

    def get_queryset(self):
        """ Делаем доступ к объектам только для владельцев(создателей) """

        if self.request.user.role == UserRoles.MODERATOR:
            return Courses.objects.all()
        else:
            return Courses.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """ Запрещаем модераторам создавать курсы """

        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вам нельзя создавать курсы")
        else:
            new_payment = serializer.save()
            new_payment.owner = self.request.user
            new_payment.save()

    def perform_destroy(self, instance):
        """ Запрещаем модераторам удалять курсы """

        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вам нельзя удалять курсы!")
        instance.delete()


class LessonCreateAPIView(generics.CreateAPIView):
    """Generic создания урока Lesson"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsPaymentOwner]

    def perform_create(self, serializer):
        """ Запрещаем модераторам создавать уроки """
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создавать уроки")
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()