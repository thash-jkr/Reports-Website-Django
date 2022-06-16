from email.policy import default
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products", default="no_product.png")
    price = models.FloatField(help_text="in US dollars $")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.created.strftime('%d/%m/%Y')}"