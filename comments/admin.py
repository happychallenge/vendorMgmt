from django.contrib import admin

from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment
    list_display = ['id', 'vendor', 'content', 'created_at']
    search_fields = ['vendor__en_name', 'content']
