from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from django.db import models

from users.models import TimeStampAbstractModel


class Student(TimeStampAbstractModel):
    """
    This class defines the basic student model for the application.
    """

    number = models.CharField(max_length=10, unique=True)
    """number: number field for the student. It must be unique."""

    name = models.CharField(max_length=100)
    """name: name field for the student. Upto 100 charactes can be allowed."""

    faculty_name = models.CharField(max_length=100)
    """faculty_name: faculty_name field for the student. Upto 100 charactes can be allowed."""

    email = models.EmailField(unique=True)
    """email: email field for the student. It must be unique."""

    date_of_birth = models.DateField()
    """date of birth: date of birth field for the student. Accepts date only"""

    def __str__(self):
        """
        This method returns a string representation of the student object.
        Returns the email

        Returns:
            str: The string representation of the student.
        """
        return self.name

    @property
    def get_current_age(self):

        today = date.today()

        age = relativedelta(today, self.date_of_birth)
        return age.years
