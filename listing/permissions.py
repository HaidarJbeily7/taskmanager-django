from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound
from .models import List, Task


class AccessListTasksPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            list = List.objects.get(id=view.kwargs['list_pk'])
        except List.DoesNotExist:
            raise NotFound()
        return request.user.id == list.user_id


class AccessTaskPermission(BasePermission):
    def has_permission(self, request, view):
        list = None
        if request.method == 'POST':
            return True
        if request.method == 'GET':
            task_id = view.kwargs.get('pk')
            if task_id is None:
                return True
        if request.method in ['PATCH', 'DELETE']:
            task_id = view.kwargs.get('pk')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound()
        list = task.list
        return request.user.id == list.user_id
