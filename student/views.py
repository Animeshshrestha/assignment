from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view, inline_serializer)
from rest_framework import response, serializers, status, views, viewsets
from rest_framework.decorators import action

from .models import Student
from .serializers import (CustomPageNumberPagination, StudentEmailSerializer,
                          StudentModelSerializer)


@extend_schema_view(
    list=extend_schema(
        operation_id="List of Student API",
        description="Returns the list of all available Student",
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description="Name of student you want to search",
                required=False,
            )
        ],
        responses=StudentModelSerializer,
    ),
    create=extend_schema(
        operation_id="Create Student API",
        description="Helps to Create the Student",
        responses=StudentModelSerializer,
        request=StudentModelSerializer,
    ),
    partial_update=extend_schema(
        operation_id="Update the Student Detail API",
        description="Updates the detail of Student",
        responses=StudentModelSerializer,
        request=StudentModelSerializer,
    ),
    update=extend_schema(exclude=True),
    retrieve=extend_schema(
        operation_id="Detail of Student by ID API",
        description="Returns the detail of student by provided ID",
        responses=StudentModelSerializer,
    ),
    destroy=extend_schema(
        operation_id="Delete Student by ID API",
        description="Deletes the detail of student by provided ID",
    ),
)
class StudentModelViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):

        query_params = request.query_params
        name = query_params.get("name", None)

        if name:
            self.queryset = self.queryset.filter(name__icontains=name)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="List of Student By Age",
        description="Returns the list of student less than the age provided",
        parameters=[
            OpenApiParameter(
                name="age", type=int, description="Age of student", required=True
            )
        ],
        responses=StudentEmailSerializer,
    )
    @action(detail=False, methods=["get"], url_path="student-list-by-age")
    def get_student_list_by_age(self, request, *args, **kwargs):

        query_params = request.query_params
        age = query_params.get("age", None)

        try:
            age = int(age)
        except Exception:
            data = {"error": "Please provide valid age in integer format only"}
            return response.Response(data, status=status.HTTP_400_BAD_REQUEST)

        filtered_queryset = [qs for qs in self.queryset if qs.get_current_age < age]
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(filtered_queryset, many=True)
        return response.Response(serializer.data)


class StudentSendEmailView(views.APIView):

    serializer_class = StudentEmailSerializer

    @extend_schema(
        operation_id="Send Email To Student API",
        description="Sends Dummy Email to the student in console",
        request=StudentEmailSerializer,
        responses=inline_serializer(
            "successful_email_send_response", fields={"detail": serializers.CharField()}
        ),
    )
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"detail": "Email Send Successfully"}
        return response.Response(data, status=status.HTTP_200_OK)
