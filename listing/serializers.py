from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import List, Task


class ListSerializer(serializers.ModelSerializer):
    title = serializers.CharField().required
    percentage_incomplete_to_complete_tasks = serializers.SerializerMethodField()

    def get_percentage_incomplete_to_complete_tasks(self, list : List):
        tasks = Task.objects.filter(list=list, parent_task__isnull=True)
        number_of_incomplete_tasks = tasks.filter(is_completed=False).count()
        number_of_complete_tasks = tasks.filter(is_completed=True).count()
        percentage = self.compute_percentage(number_of_incomplete_tasks, number_of_complete_tasks)
        return percentage

    def compute_percentage(self, a, b):
        if (b == 0) and (a == 0):
            percentage = 0
        elif (b == 0):
            percentage = -1
        else:
            percentage = a / b
        return percentage
        

    def create(self, validated_data):
        user = self.context['user']
        list = List.objects.create(
            user=user,
            **validated_data
        )
        return list

    class Meta:
        model = List
        fields = ['id', 'title', 'description', 'percentage_incomplete_to_complete_tasks']


class TaskSerializer(serializers.ModelSerializer):

    list_name = serializers.SerializerMethodField()

    def get_list_name(self, obj):
        return obj.list.title

    def validate_list(self, list):
        user_id = self.context['user'].id
        if list.user.id != user_id:
            raise ValidationError('invalid data', 400)
        return list
    
    def validate_parent_task(self, parent_task):
        if parent_task is not None:
            raise ValidationError('you cannot set parent task for a task', 400)
        return parent_task


    class Meta:
        model = Task
        fields = '__all__'


class CreateSubTaskSerializer(serializers.ModelSerializer):
    
    def validate_list(self, list):
        req_list = self.context['task'].list
        if list.id != req_list.id:
            raise ValidationError('Invalid Data!', 400)
        return list

    def create(self, validated_data):
        subtask = Task.objects.create(
            parent_task=self.context['task'],
            **validated_data
        )
        return subtask

    class Meta:
        model = Task
        fields = ['id', 'title', 'list', 'is_completed', 'due_datetime', 'note', 'location', 'priority']
 
