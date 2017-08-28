from django.contrib import admin

from .models import Todo
# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    class Meta:
        model = Todo
    list_display = ['name', 'duedate', 'etype', 'created_at']
