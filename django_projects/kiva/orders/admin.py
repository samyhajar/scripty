from django.contrib import admin
from .models import OrdersItem
from unfold.admin import ModelAdmin

# Unregister the model if already registered
try:
    admin.site.unregister(OrdersItem)
except admin.sites.NotRegistered:
    pass

@admin.register(OrdersItem)
class OrdersItemAdmin(ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at")
