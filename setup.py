from setuptools import setup, find_packages

setup(
    name="django-starter",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "django",
        "django-tailwind[reload]",
        "django-browser-reload",
        "django-unfold",
        "pick",  # Changed from python-inquirer to pick
        "python-dotenv",
        "whitenoise",
        "pillow",
        "psycopg2-binary",
        "gunicorn",
        "requests",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "django-starter=django_starter.__main__:main",
        ],
    },
)