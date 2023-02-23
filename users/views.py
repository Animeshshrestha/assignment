from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   inline_serializer)
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TokenObtainPairSerializer, UserRegisterationSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        "password", "old_password", "new_password1", "new_password2"
    )
)


class UserRegistrationView(generics.CreateAPIView):

    serializer_class = UserRegisterationSerializer
    permission_classes = ()

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @extend_schema(
        operation_id="User Registration API",
        description="Creates user with given email and password",
        request=UserRegisterationSerializer,
        responses=inline_serializer(
            "sucess_registration_response",
            fields={
                "detail": serializers.CharField(
                    default="User Account Created Successfully."
                )
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": _("User Account Created Successfully.")},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserLoginView(APIView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials and email_verified status.
    """

    serializer_class = TokenObtainPairSerializer
    permission_classes = ()

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @extend_schema(
        operation_id="User Login API",
        description="""
            Takes a set of user credentials and returns an access and refresh JSON web
            token pair to prove the authentication of those credentials.
            Set of user credentials might must be combination of email and password
        """,
        request=TokenObtainPairSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name="sucessful_user_login_response",
                fields={
                    "access_token": serializers.CharField(),
                    "refresh_token": serializers.CharField(),
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
