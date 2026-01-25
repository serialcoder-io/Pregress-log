from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin, 
    Group, Permission
)
from django.utils.translation import gettext_lazy as _
import uuid

# --------------------------
# Custom User
# --------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    first_name = models.CharField(verbose_name=_('first name'), max_length=30, blank=True)
    last_name = models.CharField(verbose_name=_('last name'), max_length=30, blank=True)
    avatar = models.ImageField(verbose_name=_('profile photo'), upload_to="avatars/", blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False)
    date_joined = models.DateTimeField(verbose_name=_('date joined'), auto_now_add=True)
    
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name=_('user groups'))
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True, verbose_name=_('user permissions'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'

