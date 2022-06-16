
from rest_framework import serializers
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

