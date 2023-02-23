from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class TimeStampAbstractModel(models.Model):
    """Inherit from this class to add timestamp fields in the model class"""

    created_at = models.DateTimeField(auto_now_add=True)
    """datetime: date on which the instance is created."""
    updated_at = models.DateTimeField(auto_now=True)
    """datetime: date on which the instance is updated."""

    class Meta:
        abstract = True


class User(AbstractUser, TimeStampAbstractModel):
    """
    This class defines the basic user model for the application.
    """

    email = models.EmailField(_("Email Address"), unique=True, null=True, blank=True)
    """email: email field for the user. It must be unique."""

    username = models.CharField(
        _("username"), max_length=150, null=True, blank=True, unique=True
    )
    """str: A unique username for the user. It must be unique, can be nullable and blank."""

    first_name = None  # type: ignore
    last_name = None  # type: ignore

    USERNAME_FIELD = "email"
    """Field that will be used as unique identifier for the user."""

    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    """Custom manager for user model."""

    def __str__(self):
        """
        This method returns a string representation of the user object.
        Returns the email

        Returns:
            str: The string representation of the user.
        """
        return self.email
