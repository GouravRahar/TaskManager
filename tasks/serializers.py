from rest_framework import serializers
from tasks.models import TaskDetail, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetail
        fields = ['id', 'name', 'description', 'created_at', 'task_type', 
                 'completed_at', 'status']
        read_only_fields = ['created_at'] 


class TaskDetailSerializer(serializers.ModelSerializer):
    # assigned_users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = TaskDetail
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at', 
                  'task_type', 
                 'completed_at', 
                 'status',] 
                #  'assigned_users']
        read_only_fields = ['created_at']


class TaskAssignSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True
    )

    def validate_task_id(self, value):
        if not TaskDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("Task does not exist")
        return value

    def validate_user_ids(self, value):
        invalid_ids = [uid for uid in value if not User.objects.filter(id=uid).exists()]
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid user IDs: {invalid_ids}")
        return value