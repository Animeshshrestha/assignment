from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """
    This is a custom implementation of `UserManager` class provided by django for
    handling creation and management of user objects.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.

        Args:
            email (str): A valid email address of the user
            password (str): Password for the user.

        Raises:
            ValueError: If email is empty.

        Returs:
            user (object): The created user object.
        """
        if not email:
            raise ValueError("The Email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.

        Args:
            email (str): Email address of the user.
            password (str): Password for the user.

        Keyword Args:
            extra_fields (dict): Additional fields for the user object.

        Returns:
            user (User): The created user object.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.

        Args:
            email (str): Email address of the user.
            password (str): Password for the user.

        Keyword Args:
            extra_fields (dict): Additional fields for the user object.

        Returns:
            user (User): The created user object.

        Raises:
            ValueError: if is_staff or is_superuser fields are not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
