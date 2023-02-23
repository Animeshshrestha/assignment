from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from .models import Student


class CustomPageNumberPagination(PageNumberPagination):

    page_size = 200
    page_size_query_param = "page_size"
    max_page_size = 200


def send_email(request, email):

    subject = "Test Email Send To User"
    from_email = "testemail@student.com"
    to = [email]
    email_template_name = "email_templates/student_email.txt"
    html_email_template_name = "email_templates/student_email.html"
    current_site = get_current_site(request)
    site_name = current_site.name
    context = {"site_name": site_name}
    text_content = loader.render_to_string(email_template_name, context)
    html_content = loader.render_to_string(html_email_template_name, context)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "number", "name", "faculty_name", "email", "date_of_birth"]

    def validate_date_of_birth(self, value):

        current_date = datetime.now().date()
        if current_date < value:
            raise serializers.ValidationError(
                {"error": "Date Of birth cannot be greater than today's date"}
            )
        return value


class StudentEmailSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    def validate_email(self, value):

        email = value.lower()
        if not Student.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"error": f"Student with email {email} does not exists"}
            )
        return email

    def create(self, validated_data):

        email = validated_data["email"]
        request = self.context["request"]

        send_email(request, email)
        return validated_data
