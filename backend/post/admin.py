from django.contrib import admin
from .models import Post


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish_date', 'category')
    ordering = ('-publish_date',)
    list_display_links = ('id', 'title')
    search_fields = ('title', 'category', 'content')
    list_per_page = 25


# Register your models here.
admin.site.register(Post, PostsAdmin)
