# File: django_starter/__init__.py

from .core.base_installer import BaseInstaller
from .core.django_installer import DjangoInstaller
from .core.tailwind_installer import TailwindInstaller
from .templates.base_template_creator import BaseTemplateCreator
from .templates.app_template_creator import AppTemplateCreator

__version__ = "1.0.0"
