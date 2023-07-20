from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin

from university.common.models import SoftDeletedUUIDModel


class UsersManager(BaseUserManager['Users']):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class SoftDeleteUsersManager(UsersManager):
    """
    will be excluded deleted objects from queryset
    """

    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at__isnull=False)


class Users(AbstractBaseUser, PermissionsMixin, SoftDeletedUUIDModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    birthday = models.DateField(null=True)

    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = SoftDeleteUsersManager()
    all_objects = UsersManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username
