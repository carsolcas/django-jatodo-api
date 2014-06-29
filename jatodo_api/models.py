# -*- coding: UTF-8 -*-

# Import from Django
from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, CharField
from django.db.models import TextField,  DateField, DateTimeField
from django.db.models import PositiveIntegerField, PositiveSmallIntegerField
from django.utils.translation import ugettext_lazy as _


PENDING = 0
IN_PROGRESS = 2
FINISHED = 3


class Project(Model):
    name = CharField(_('name'), max_length=80)
    description = TextField(_('description'), blank=True)
    owner = ForeignKey(User)

    def __unicode__(self):
        return self.name


class Task(Model):
    STATE_CHOICES = (
        (PENDING, _('pending')),
        (IN_PROGRESS, _('in progress')),
        (FINISHED, _('finished')),
    )
    project = ForeignKey(Project)
    title = CharField(_('title'), max_length=100)
    description = TextField(_('description'), blank=True)
    actual_user = ForeignKey(User, blank=True, null=True)
    state = PositiveSmallIntegerField(max_length=2,  default=PENDING,
                            choices=STATE_CHOICES)
    total_time = PositiveIntegerField(_('total time'), default=0)

    def __unicode__(self):
        return self.title


class TaskTime(Model):
    user = ForeignKey(User)
    task = ForeignKey(Task)
    start_date = DateTimeField(_('start date'))
    end_date = DateTimeField(_('End date'))

    def __unicode__(self):
        return "%s - %s" % (self.task.title, self.user.username)
