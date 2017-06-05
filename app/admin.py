from django.contrib import admin

from app.models import List, Task


class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )
    ordering = ('id', )

admin.site.register(List, ListAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'list', 'title', 'completed')
    search_fields = ('title', )
    ordering = ('id', )

admin.site.register(Task, TaskAdmin)