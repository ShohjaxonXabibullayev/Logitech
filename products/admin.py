from django.contrib import admin
from .models import *
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'user']
    list_filter = ['category', 'user']
    search_fields = ['title__icontains']

admin.site.register(Techs, ProductsAdmin)
admin.site.register(Catagory)
admin.site.register(Comment)
