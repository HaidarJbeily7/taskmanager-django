
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import List, Task
from .serializers import  ListSerializer, TaskSerializer, CreateSubTaskSerializer
from .permissions import AccessListTasksPermission, AccessTaskPermission

class BaseDestroyModelMixin(DestroyModelMixin):
     def destroy(self, request, *args, **kwargs):
        is_soft = request.data.get('soft_delete')
        if is_soft != '1':
            return super().destroy(request, *args, **kwargs)
        instance  = super().get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListViewSet(CreateModelMixin, 
                ListModelMixin, 
                UpdateModelMixin, 
                BaseDestroyModelMixin, 
                GenericViewSet):

    http_method_names = ['post', 'get', 'patch', 'delete']
    
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = List.objects.all()
        else:
            queryset = List.objects.filter(user_id=user.id)
        return queryset

    def get_serializer_context(self):
        return {'user' : self.request.user}    


class ListTasksViewSet(ListModelMixin, GenericViewSet):

    http_method_names = ['get']
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, AccessListTasksPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get_queryset(self):
        queryset = Task.objects.filter(list_id=self.kwargs['list_pk'], parent_task__isnull=True)
        return queryset


class TaskViewSet(ModelViewSet, BaseDestroyModelMixin):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, AccessTaskPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    @action(detail=True, methods=['GET', 'POST'])
    def subtasks(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        if task.parent_task is not None:
            raise ValidationError({'task':'invalid id'}, 400)

        if request.method == 'GET':
            subtasks = Task.objects.filter(parent_task=task_id)
            serializer = TaskSerializer(subtasks, many=True)
            return Response(serializer.data, 200)

        if request.method =='POST':
            serializer = CreateSubTaskSerializer(data=request.data, context={'task':task})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        


    def list(self, request, *args, **kwargs):
        tasks = self.get_queryset().filter(parent_task__isnull=True)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Task.objects.all()
        else:
            tasks = Task.objects.select_related('list')
            list_data = []
            for task in tasks:
                if task.list.user_id == user.id:
                    list_data.append(task.id)
            queryset = Task.objects.filter(id__in=list_data)
        return queryset
        
    def get_serializer_context(self):
        return {'user' : self.request.user}   
        