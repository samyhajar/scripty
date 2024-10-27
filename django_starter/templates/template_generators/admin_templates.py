"""Admin template generator for Django apps."""

def get_admin_template(app_name, model_name, list_display, search_fields, list_filter, is_main_app=False):
    """Generate admin.py content for the app."""

    if is_main_app:
        return f'''from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from .models import {model_name}
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

# Unregister default User and Group models
try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

# Unregister the model if already registered
try:
    admin.site.unregister({model_name})
except admin.sites.NotRegistered:
    pass

@admin.register({model_name})
class {model_name}Admin(ModelAdmin):
    list_display = {list_display}
    search_fields = {search_fields}
    list_filter = {list_filter}
'''
    else:
        return f'''from django.contrib import admin
from .models import {model_name}
from unfold.admin import ModelAdmin

# Unregister the model if already registered
try:
    admin.site.unregister({model_name})
except admin.sites.NotRegistered:
    pass

@admin.register({model_name})
class {model_name}Admin(ModelAdmin):
    list_display = {list_display}
    search_fields = {search_fields}
    list_filter = {list_filter}
'''