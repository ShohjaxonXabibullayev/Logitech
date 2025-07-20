from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'sent_at']
    search_fields = ['full_name', 'email', 'message']
    list_filter = ['sent_at']

admin.site.register(Contact, ContactAdmin)
# Register your models here.
