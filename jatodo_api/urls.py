# -*- coding: UTF-8 -*-

# Import from Django
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from .views import ProjectsView, ProjectView


urlpatterns = patterns('',
    url(r'^projects/$', ProjectsView.as_view(), name='todo-projects'),
    url(r'^projects/(?P<project_id>\d+)/$', ProjectView.as_view(),
        name='todo-project'),
)
