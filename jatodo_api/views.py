# -*- coding: UTF-8 -*-
from datetime import datetime

# Import from Django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

# Import from Django Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

# Import from here
from .models import Project, Task, TaskTime

mask_date = '%Y%m%d%H%M%S'

def response_created(item_id, url):
    r = Response("%i" % (item_id), status=201, content_type='text/plain')
    r['Location'] = url
    return r

def get_project_data(project):
    return {"name": project.name,
            "id": project.id,
            "description": project.description}

def get_time_data(time):
    return {"user": time.user.id,
            "id": time.id,
            "task": time.task.id,
            "start_date":time.start_date.strftime(mask_date ),
            "end_date":time.end_date.strftime(mask_date ),
            }

def get_project(request, project_id, mode="r"):
    return get_object_or_404(Project, pk=project_id)

def get_task(request, task_id, mode="r"):
    return get_object_or_404(Task, pk=task_id)

def get_task_data(task):
    return {"title": task.title,
            "id": task.id,
            "project": task.project.id,
            "actual_user": task.actual_user.id,
            "total_time": task.total_time,
            "state": task.state,
            "description": task.description}


class ProjectView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kw):
        project = get_project(request, kw['project_id'])
        return Response(get_project_data(project))

    def post(self, request, *args, **kwargs):
        """
        Update project

        Required parameters:
        - **project_id**: The internal ID of the project. Type: Integer.
        """
        project = get_project(request, kwargs['project_id'], mode='w')
        fields = ('name', 'description')
        for f in fields:
            if f in request.POST:
                setattr(project, f, request.POST[f])
        project.save()
        return Response('', status=200)

    def delete(self, request, *args, **kw):
        """
        Delete project

        Required parameters:
        - **project_id**: The internal ID of the project. Type: Integer.
        """
        project = get_project(request, kw['project_id'], mode='w')
        project.delete()
        return Response('', status=204)


class ProjectsView(APIView):
    """List Projects"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """ Create new project.

        Parameters:
        - **name**: The name of the project. Type: String.
        - **description**: The Description of the project. Type: Text. Optional
        """
        user = request.user
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if not name:
            msg = _("Name field is mandatory")
            return Response('{"detail": %s }' % msg, status=501)

        project = Project(name=name, description=description, owner=user)
        project.save()
        url = reverse('todo-project', args=(project.id,))
        return response_created(project.id, url)

    def get(self, request, *args, **kwargs):
        """Get list of projects in json format. """
        projects = Project.objects.all()
        data = [ get_project_data(p) for p in projects ]
        return Response(data)


class TasksView(APIView):
    """List tasks"""
    permission_classes = (IsAuthenticated,)
    required_fields = [{'field_name':'title',
                        'msg':_("Name field is mandatory"),},
                       {'field_name':'description',
                        'msg':_("Description field is mandatory"),}]

    def post(self, request, *args, **kwargs):
        """ Create new task.

        Parameters:
        - **project**: Id of the related project. Type: Integer.
        - **title**: The title of the task. Type: Text.
        - **description**: The Description of the task. Type: Text.
        """
        actual_user = request.user
        project_id = request.POST.get('project', '')

        data = {'actual_user': actual_user,
                'title':request.POST.get('title', ''),
                'description':request.POST.get('description', ''),
                'project':get_object_or_404(Project, pk=project_id),
               }

        for field in self.required_fields:
            if not data[field['field_name']]:
                return Response('{"detail": %s }' % msg, status=501)

        task = Task(**data)
        task.save()
        url = reverse('todo-task', args=(task.id,))
        return response_created(task.id, url)

    def get(self, request, *args, **kwargs):
        """Get list of projects in json format. """
        tasks = Task.objects.all()
        data = [ get_task_data(t) for t in tasks ]
        return Response(data)


class TaskView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kw):
        """
        Delete task

        Required parameters:
        - **task_id**: The internal ID of the task. Type: Integer.
        """
        task = get_task(request, kw['task_id'], mode='w')
        task.delete()
        return Response('', status=204)

    def get(self, request, *args, **kw):
        """
        Get task info

        Required parameters:
        - **task_id**: The internal ID of the task. Type: Integer.
        """
        task = get_task(request, kw['task_id'])
        return Response(get_task_data(task))


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
