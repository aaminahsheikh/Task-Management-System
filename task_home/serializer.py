from rest_framework import serializers

from task_home.models import User, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

        def create(self, validated_data):
            password = validated_data.pop('password', None)
            user = super(UserSerializer, self).create(validated_data)
            if password:
                user.set_password(password)
                user.save()
            return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
