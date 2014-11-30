# -*- coding: UTF-8 -*-

# Import from Django
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from .views import ProjectList, ProjectDetail
from .views import TaskTimeView, TaskList, TaskDetail


urlpatterns = patterns('',
    url(r'^projects/$', ProjectList.as_view(), name='projects-list'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(),
        name='project-detail'),

    url(r'^tasks/$', TaskList.as_view(), name='tasks-list'),
    url(r'^tasks/(?P<pk>\d+)/$', TaskDetail.as_view(), name='task-detail'),

    url(r'^tasks/(?P<task_id>\d+)/time/$', TaskTimeView.as_view(),
        name='tasktime-list'),
)
