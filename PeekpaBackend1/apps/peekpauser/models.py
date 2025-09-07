from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from shortuuidfield import ShortUUIDField

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from apps.api.authentications import PeekpaAccessToken

class PeekpaUserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('邮箱格式不正确.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin_user(self, email, password):
        if not email:
            raise ValueError('邮箱格式不正确.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_UNKNOWN = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_ITEMS = (
        (GENDER_MALE, '男'),
        (GENDER_FEMALE, '女'),
        (GENDER_UNKNOWN, '未设置'),
    )

    uid = ShortUUIDField(primary_key=True, unique=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.PositiveIntegerField(default=GENDER_UNKNOWN, choices=GENDER_ITEMS)
    details = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    data_join = models.DateTimeField(verbose_name='data join', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    objects = PeekpaUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def name(self):
        return "{} {}".format(self.last_name, self.first_name)
        
    def token(self):
        refresh = PeekpaAccessToken.for_user(self)
        return str(refresh)
    
class Avatar(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    url = models.URLField()