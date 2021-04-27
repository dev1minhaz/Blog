from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_description', 'created_at', 'user')
    ordering = ('-created_at',)
    list_display_links = ('id',)
    search_fields = ('content', 'user')
    list_per_page = 25


# Register your models here.
admin.site.register(Comment, CommentAdmin)
