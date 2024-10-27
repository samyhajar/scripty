import subprocess
import sys
from pathlib import Path

class UnfoldInstaller:
    def __init__(self, project_name):
        self.base_dir = Path.cwd()
        self.project_name = project_name
        self.main_app = 'home'  # Fixed main app name
        self.settings_path = self.base_dir / project_name / "settings.py"
        self.admin_path = self.base_dir / self.main_app / "admin.py"

    def install(self):
        """Main installation method for Django Unfold."""
        try:
            # 1. Install Django Unfold package
            self.install_unfold_package()

            # 2. Update settings to include Unfold
            self.update_settings()

            # 3. Update admin.py to use Unfold's ModelAdmin
            self.update_admin()

            print("\nDjango Unfold has been successfully installed and configured!")
        except Exception as e:
            raise Exception(f"Unfold setup failed: {str(e)}")

    def install_unfold_package(self):
        """Install Django Unfold package."""
        print("\nInstalling Django Unfold...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "django-unfold"],
            check=True,
        )
        print("Django Unfold installed successfully!")

    def update_settings(self):
        """Add Unfold configuration to settings."""
        with open(self.settings_path, "r") as file:
            content = file.readlines()

        # Add Unfold to the beginning of INSTALLED_APPS
        for i, line in enumerate(content):
            if "INSTALLED_APPS = [" in line:
                insert_index = i + 1
                content.insert(insert_index, "    'unfold',\n")
                content.insert(insert_index, "    'unfold.contrib.filters',\n")
                content.insert(insert_index, "    'unfold.contrib.forms',\n")
                content.insert(insert_index, "    'unfold.contrib.inlines',\n")
                content.insert(insert_index, "    'unfold.contrib.import_export',\n")
                content.insert(insert_index, "    'unfold.contrib.guardian',\n")
                content.insert(insert_index, "    'unfold.contrib.simple_history',\n")
                break

        with open(self.settings_path, "w") as file:
            file.writelines(content)
        print("Updated settings with Unfold")

    def update_admin(self):
        """Update admin.py to use Unfold's ModelAdmin."""
        print("\nUpdating admin.py to use Unfold's ModelAdmin...")
        admin_content = f"""from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import HomeItem

# Unregister the default User and Group models
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

# Register your own models using Unfold's ModelAdmin
@admin.register(HomeItem)
class HomeItemAdmin(ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at")
"""
        with open(self.admin_path, "w") as file:
            file.write(admin_content)
        print("Updated admin.py successfully!")