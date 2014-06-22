# -*- coding: UTF-8 -*-

# Import from Django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

# Import from Django Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

# Import from here
from .models import Project, Task


def response_created(item_id, url):
    r = Response("%i" % (item_id), status=201, content_type='text/plain')
    r['Location'] = url
    return r


def get_project_data(project):
    return {"name": project.name,
            "id": project.id,
            "description": project.description}

def get_project(request, project_id, mode="r"):
    return get_object_or_404(Project, pk=project_id)


class ProjectView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kw):
        project = get_project(request, kw['project_id'])
        return Response(get_project_data(project))


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
        user = request.user
        projects = Project.objects.all()
        data = [ get_project_data(p) for p in projects ]
        return Response(data)
