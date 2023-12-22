from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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
        created_by_uuid = request.data.get('created_by')
        user = get_object_or_404(User, id=created_by_uuid)

        task_data = request.data
        task_data.update({'created_by': user.id})
        serializer = TaskSerializer(data=task_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
