from django.contrib import admin

# Register your models here.
from .models import Properties, SavedProperty
from .models import ContactMessage


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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('email', 'name', 'subject', 'sent', 'created_at')
	list_filter = ('sent', 'created_at')
	search_fields = ('email', 'name', 'subject', 'message')
