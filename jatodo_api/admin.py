"""Admin"""

# Import from Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Import from Pilot-Academy
from .models import Project, Task, TaskTime


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','owner')
    raw_id_fields = ('owner',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'state', 'project')


class TaskTimeAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'start_date', 'end_date')
    fieldsets = ((_('Task info'), {'fields': ('task', 'user',)}),
                 (_('Time'), {'fields': ('start_date', 'end_date',)}),)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskTime, TaskTimeAdmin)
