# File: setup.py

from setuptools import setup, find_packages

setup(
    name="django-starter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "django",
        "django-tailwind[reload]",
    ],
    entry_points={
        "console_scripts": [
            "django-starter=django_starter.__main__:main",
        ],
    },
)