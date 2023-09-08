from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from rest_framework.authtoken.models import Token

from user.manager import UserManager

# Переменная, которая позволяет не заполнять поле модели
NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """Класс для ролей пользователя"""
    USER = 'user',
    ADMIN = 'admin'


class User(AbstractBaseUser):
    """Класс кастомного пользователя
    в котором переопределяем параметры
    для корректной работы djoser
    и убираем username, меняя авторизацию на email"""

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    username = None
    first_name = models.CharField(max_length=35, verbose_name='имя')
    last_name = models.CharField(max_length=35, verbose_name='фамилия')
    phone = models.CharField(
        unique=True,
        max_length=35,
        verbose_name='телефон'
    )
    email = models.EmailField(unique=True, verbose_name='почта')
    image = models.ImageField(
        upload_to='users/',
        verbose_name='аватар',
        **NULLABLE
    )
    role = models.CharField(
        max_length=9,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        **NULLABLE
    )
    is_active = models.BooleanField(verbose_name='активный', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    # Переопределяем менеджер объектов
    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    # получение токена пользователя
    def get_my_token(self):
        return Token.objects.get(user=self)

    my_token = property(get_my_token)
