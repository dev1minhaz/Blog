from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    ordering = ('id',)
    list_display_links = ('id', 'name')
    search_fields = ('name', 'user')
    list_per_page = 25


# Register your models here.
admin.site.register(Tag, TagAdmin)
