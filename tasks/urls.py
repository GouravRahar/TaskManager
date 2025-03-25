from django.urls import path
from tasks.views import CreateTaskView, AssignTaskView, UserTasksView

urlpatterns = [
    path('tasks/create/', CreateTaskView.as_view(), name='create_task'),
    path('tasks/assign/', AssignTaskView.as_view(), name='assign_task'),
    path('users/<int:user_id>/tasks/', UserTasksView.as_view(), name='user_tasks'),
]