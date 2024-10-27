from setuptools import setup, find_packages

setup(
    name="django-starter",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "django>=4.0",
        "django-tailwind[reload]>=3.0",
    ],
    entry_points={
        "console_scripts": [
            "django-starter=django_starter.__main__:main",
        ],
    },
)
