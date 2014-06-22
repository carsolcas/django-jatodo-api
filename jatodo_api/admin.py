"""Admin"""

# Import from Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Import from Pilot-Academy
from .models import Project, Task


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','owner')
    raw_id_fields = ('owner',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'state', )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
