from django.contrib import admin

# Register your models here.
from .models import Properties, SavedProperty


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
	list_display = ("name", "type", "location", "price", "category", "status", "is_featured")
	list_filter = ("type", "category", "status", "is_featured")
	search_fields = ("name", "location", "description")


@admin.register(SavedProperty)
class SavedPropertyAdmin(admin.ModelAdmin):
	list_display = ("user", "property", "is_paid", "saved_at")
	list_filter = ("is_paid", "saved_at")
	search_fields = ("user__username", "user__email", "property__name", "property__location")
