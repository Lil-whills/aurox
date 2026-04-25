from django.contrib import admin

# Register your models here.
from .models import Properties


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
	list_display = ("name", "type", "location", "price", "category", "status", "is_featured")
	list_filter = ("type", "category", "status", "is_featured")
	search_fields = ("name", "location", "description")
