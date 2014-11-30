# -*- coding: UTF-8 -*-
from datetime import datetime

# Import from Django
from django.shortcuts import get_object_or_404

# Import from Django Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions

# Import from here
from .models import Project, Task, TaskTime
from .serializers import TaskSerializer, ProjectSerializer

mask_date = '%Y%m%d%H%M%S'

def response_created(item_id, url):
    r = Response("%i" % (item_id), status=201, content_type='text/plain')
    r['Location'] = url
    return r

def get_time_data(time):
    return {"user": time.user.id,
            "id": time.id,
            "task": time.task.id,
            "start_date":time.start_date.strftime(mask_date ),
            "end_date":time.end_date.strftime(mask_date ),
            }

def get_task(request, task_id, mode="r"):
    return get_object_or_404(Task, pk=task_id)


class ProjectList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    model = Project
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer

    model = Project



class TaskList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    model = Task
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TaskSerializer

    model = Task


class TaskTimeView(APIView):
    permission_classes = (IsAuthenticated,)

    def parse_date(self, field):
        d = self.request.POST.get(field, '')
        return datetime.strptime(d, mask_date) if d else ''

    def post(self, request, *args, **kwargs):
        """ Create new time task.

        Parameters:
        - **start_date**:Start date time of the task Type: Text. yyyymmdHHMMSS
        - **end_date**:End date time of the task Type: Text. yyyymmdHHMMS
        """
        user = request.user
        task = get_object_or_404(Task, pk=kwargs['task_id'])

        start_date = self.parse_date('start_date')
        end_date = self.parse_date('end_date')
        tt = TaskTime(user=user, task=task, 
                start_date=start_date, end_date=end_date)
        tt.save()
        url = reverse('todo-task', args=(tt.id,))
        return response_created(task.id, url)

    def get(self, request, *args, **kwargs):
        """Get list of projects in json format. """
        task = get_task(request, kwargs['task_id'], mode='w')
        times = TaskTime.objects.filter(task=task).order_by('start_date')
        data = [ get_time_data(t) for t in times ]
        return Response(data)
