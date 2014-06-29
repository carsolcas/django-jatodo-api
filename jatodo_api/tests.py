"""Tests for pilot_academy.api"""
import base64
import json

from hashlib import md5
from datetime import date, time, datetime, timedelta

from django.test import TestCase

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Import from here
from .models import Project, Task, TaskTime

class APIBaseCase(TestCase):
    def setUp(self):
        """Create an UserProfile"""
        self.login = 'carsol'
        self.email = 'carlos@gmail.com'
        self.password = '123'
        self.auth_string = 'Basic %s' % base64.encodestring(
            '%s:%s' % (self.login, self.password))[:-1]

        self.user = User.objects.create_user(
            self.login, self.email, self.password)

        self.detail_error = 'Authentication credentials were not provided.'


class APIProjectCase(APIBaseCase):
    def test_projects(self):
        url = reverse('todo-projects')

        # Get projects without login
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEquals(content['detail'], self.detail_error)

        # Get projects with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(content, [])

        # Create new project without login
        response = self.client.post(url)
        self.assertEquals(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEquals(content['detail'], self.detail_error)

        # Create new project with login
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 501)

        project_title = 'test project'
        response = self.client.post(url,
                        {'name':project_title,
                         'description':'description'},
                        HTTP_AUTHORIZATION=self.auth_string,
                        )
        self.assertEquals(response.status_code, 201)

        # Get projects with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(len(content), 1)
        self.assertEquals(content[0]['name'], project_title)

    def test_project(self):
        project = Project(name='Project title',
                          description='Description text',
                          owner=self.user)
        project.save()

        url = reverse('todo-project', args=(1,))

        #Get project without login
        response = self.client.post(url)
        self.assertEquals(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEquals(content['detail'], self.detail_error)

        #Get project with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(content['name'], 'Project title')

        #Update project with login
        response = self.client.post(url, 
                {'description':'New description',},
                HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(content['description'], 'New description')

        #Delete project
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 204)

        #Now get the object again
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 404)


class APITaskCase(APIBaseCase):
    def setUp(self):
        super(APITaskCase, self).setUp()
        self.project = Project(name='Project title',
                          description='Description text',
                          owner=self.user)
        self.project.save()

    def test_tasks(self):
        url = reverse('todo-tasks')

        # Get tasks without login
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEquals(content['detail'], self.detail_error)

        # Get tasks with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(content, [])

        # Create new task
        response = self.client.post(url,{'project':1,
                                         'user':1,
                                         'title':'Task Title',
                                         'description':'Task Description',
                                        },
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEquals(len(content), 1)

        # Get tasks with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(len(content), 1)

    def test_task(self):
        task = Task(title='Task title',
                    description='Description text',
                    project=self.project,
                    actual_user=self.user)
        task.save()

        url = reverse('todo-task', args=(1,))

        #Get task with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(content['title'], 'Task title')

        #Delete task
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 204)

        #Now get the object again
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 404)


class APITaskTimeCase(APIBaseCase):
    def setUp(self):
        super(APITaskTimeCase, self).setUp()
        self.project = Project(name='Project title',
                          description='Description text',
                          owner=self.user)
        self.project.save()

        task = Task(title='Task title',
                    description='Description text',
                    project=self.project,
                    actual_user=self.user)
        task.save()

    def test_tasktime(self):
        url = reverse('todo-tasktime', args=(1,))

        # Get tasks without login
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEquals(content['detail'], self.detail_error)

        # Get tasks with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(content, [])

        # Create new task time
        response = self.client.post(url,{'start_date':'20140629170001',
                                         'end_date':'20140629174433',
                                        },
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEquals(len(content), 1)

        # Get tasks with login
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(len(content), 1)
