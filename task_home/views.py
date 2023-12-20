from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from task_home.serializer import UserSerializer, TaskSerializer
from task_home.models import User, Task


# Create your views here.
def home(request):
    return HttpResponse("hello, Amina!")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        users = self.queryset
        return Response(self.serializer_class(users, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if 'password' not in request.data:
            return Response({'error': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['password'] = make_password(request.data['password'])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data.get('created_by')
        user = User.objects.filter(id=user_id).first()
        print("========", user)
        if not user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        assigned_to_id = serializer.validated_data.get('assigned_to')
        if not assigned_to_id:
            user_id = user
        else:
            user_id = User.objects.filter(id=assigned_to_id).first()
        print(user_id, "==========")
        task = Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            status=request.POST.get('status'),
            due_date=request.POST.get('due_date'),
            created_by=user,
            assigned_to=user_id
        )

        return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)
