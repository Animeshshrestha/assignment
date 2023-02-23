from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserRegisterationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_name = data["username"]
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        mesg = "This email has been already registered."
        if User.objects.filter(username=user_name).exists():
            raise serializers.ValidationError({"error": mesg})
        if password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords don't match."})
        if password:
            user = User(username=user_name)
            try:
                validate_password(password=password, user=user)
            except Exception as e:
                raise serializers.ValidationError({"error": e.messages})
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("User Name"), required=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        user_name = attrs.get("username", None)
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=user_name, password=password
        )
        if not user:
            msg = {"error": "Unable to log in with provided credentials."}
            raise serializers.ValidationError(msg, code="authorization")
        refresh = self.get_token(user)
        response = {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }
        request = self.context["request"]
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return response

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
