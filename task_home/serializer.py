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
    created_by = serializers.CharField(write_only=True)
    assigned_to = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with ID {user_id} does not exist.")

    def create(self, validated_data):
        created_by_id = validated_data.pop('created_by')
        assigned_to_id = validated_data.pop('assigned_to', None)
        created_by = self.get_user(created_by_id)
        assigned_to = self.get_user(assigned_to_id) if assigned_to_id else created_by

        task = Task.objects.create(created_by=created_by, assigned_to=assigned_to, **validated_data)
        return task
