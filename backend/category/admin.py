from .models import Category
from django.contrib import admin

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    ordering = ("name",)
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_per_page = 25


admin.site.register(Category, CategoryAdmin)
