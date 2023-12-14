from rest_framework import serializers

from main.models import Payments

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для юзера"""

    # Вложенный сериализатор платежей
    payments = serializers.SerializerMethodField()

    class Meta:
        # показываем все поля
        model = User
        fields = '__all__'


class PublicUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для публичной информации о пользователе """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'role']