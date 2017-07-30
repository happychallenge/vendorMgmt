from django.contrib import admin


from .models import Event
# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    class Meta:
        model = Event
    list_display = ['id', 'name', 'num', 'porder', 'etype', 'event_date']
    list_display_links = ['name', 'porder']