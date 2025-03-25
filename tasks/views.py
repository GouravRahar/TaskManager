from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models import TaskDetail, User
from tasks.serializers import TaskCreateSerializer, TaskDetailSerializer, TaskAssignSerializer, UserSerializer

class CreateTaskView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignTaskView(APIView):
    def post(self, request):
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            task = TaskDetail.objects.get(id=serializer.validated_data['task_id'])
            users = User.objects.filter(id__in=serializer.validated_data['user_ids'])
            task.assigned_users.set(users)
            return Response(TaskDetailSerializer(task).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserTasksView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            tasks = TaskDetail.objects.filter(assigned_users=user)
            serializer = TaskDetailSerializer(tasks, many=True)
            return Response({
                'user': UserSerializer(user).data,
                'tasks': serializer.data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)