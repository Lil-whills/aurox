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
	list_display = ('name', 'email', 'phone', 'message_snippet', 'sent', 'created_at', 'error_snippet')
	list_filter = ('sent', 'created_at')
	search_fields = ('email', 'name', 'subject', 'message', 'error', 'phone')

	def message_snippet(self, obj):
		if not obj.message:
			return ''
		return (obj.message[:200] + '...') if len(obj.message) > 200 else obj.message
	message_snippet.short_description = 'Message (snippet)'

	def error_snippet(self, obj):
		if not obj.error:
			return ''
		return (obj.error[:200] + '...') if len(obj.error) > 200 else obj.error
	error_snippet.short_description = 'Error (snippet)'
