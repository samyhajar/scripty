from django.contrib import admin
from .models import ClientsItem
from unfold.admin import ModelAdmin

# Unregister the model if already registered
try:
    admin.site.unregister(ClientsItem)
except admin.sites.NotRegistered:
    pass

@admin.register(ClientsItem)
class ClientsItemAdmin(ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at")
