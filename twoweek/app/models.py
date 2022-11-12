from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


# Create your models here.\
class Genre(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Введите жанр книги (например, научная фантастика, французская поэзия и т. д.).")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 символьный номер')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для этой книги")

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


from datetime import datetime
from email.policy import default
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse


# Создаем класс менеджера пользователей
class MyUserManager(BaseUserManager):
    # Создаём метод для создания пользователя
    def _create_user(self, email, username, password, **extra_fields):
        # Проверяем есть ли Email
        if not email:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Email")
        # Проверяем есть ли логин
        if not username:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Логин")
        # Делаем пользователя
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, email, username, password):
        # Возвращаем нового созданного пользователя
        return self._create_user(email, username, password)

    # Делаем метод для создание админа сайта
    def create_superuser(self, email, username, password):
        # Возвращаем нового созданного админа
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Введите категорию заявки')

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=50, help_text="Напишите ФИО")
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=254)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # Идентификатор для обращения
    REQUIRED_FIELDS = ['email']  # Список имён полей для Superuser

    objects = MyUserManager()

    def __str__(self):
        return self.full_name


class Application(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    title = models.CharField(max_length=200, verbose_name='Название')
    desc = models.TextField(max_length=400, verbose_name='Описание')
    img = models.ImageField(upload_to='img', verbose_name='Картинка')
    ready_design = models.ImageField(upload_to='design', verbose_name='Готовый дизайн', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True,
                             to_field='id')
    date = models.DateField(default=datetime.today())
    comment = models.TextField(max_length=400, verbose_name='Комментарий', null=True, blank=True)

    NEW = 'new'
    LOAD = 'load'
    READY = 'ready'
    LOAN_STATUS = (
        (NEW, 'Новая'),
        (LOAD, 'Принято в работу'),
        (READY, 'Выполнено'),
    )

    status = models.CharField(max_length=30, choices=LOAN_STATUS, default='new', help_text='Статус',
                              verbose_name='Статус')

    SKETCH = 'sketch'
    MID_DETAIL = 'mid_detail'
    AUTHOR = 'author'
    CATEGORIES = (
        (SKETCH, 'Эскизный проект'),
        (MID_DETAIL, 'Средняя детализация'),
        (AUTHOR, 'Авторский интерьер'),
    )

    category = models.CharField(max_length=30, choices=CATEGORIES, default='Эскизный проект', help_text='Категории',
                                verbose_name='Категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Тут мы создали новый метод
        return reverse('profile_application_detail', args=[str(self.id)])
