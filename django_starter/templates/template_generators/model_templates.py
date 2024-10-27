"""Model template generator for Django apps."""

def get_models_template(app_name):
    """Generate models.py content for the app."""
    if app_name == "clients":
        return '''from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
'''
    elif app_name == "orders":
        return '''from django.db import models
from clients.models import Client

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} for {self.client}"
'''
    else:
        return f'''from django.db import models

class {app_name.capitalize()}Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "{app_name.capitalize()} Item"
        verbose_name_plural = "{app_name.capitalize()} Items"
'''