# -*- coding: UTF-8 -*-
from rest_framework import serializers

# Import from here
from .models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
#    tasks = serializers.HyperlinkedIdentityField('tasks', view_name='projecttask-list',
#                                     lookup_field='id')

    class Meta:
        model = Project 
        fields = ('id', 'name', 'description', 'owner',) #'tasks', )


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(required=False)
#    tasks = serializers.HyperlinkedIdentityField('tasks', view_name='projecttask-list',
#                                     lookup_field='id')


    def get_validation_exclusions(self, instance=None):
        exclusions = super(TaskSerializer, self).get_validation_exclusions(instance)
        return exclusions + ['project']

    class Meta:
        model = Task 


