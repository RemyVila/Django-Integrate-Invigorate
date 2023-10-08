from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Add related_name to distinguish group and permission relationships
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



User = get_user_model()

class DailyInput(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wellbeing = models.PositiveIntegerField()  # You can adjust the field type as needed
    vigor = models.PositiveIntegerField()
    foods = models.JSONField(default=dict)
    hours_slept = models.IntegerField(
        default=6,
        validators=[MaxValueValidator(24), MinValueValidator(0)]
    )
    wakeup_time = models.TimeField(default=None)

    class Meta:
        verbose_name = "Daily Input"
        verbose_name_plural = "Daily Inputs"

    def __str__(self):
        return f"Daily Input for {self.user.username} on {self.date}"

