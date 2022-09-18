from django.db import models
from django.utils import timezone
from django.shortcuts import reverse

from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from .utils import generate_code

# Create your models here.
class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.price = int(self.product.price) * int(self.quantity)
        return super().save(*args, **kwargs)

    def get_sales_id(self):
        sale_obj = self.sale_set.first()
        return sale_obj.id

    def __str__(self):
        return f"{self.id} - {self.product.name}"


class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()

    def get_absolute_url(self):
        return reverse("sales:detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"Sales for the amount of ${self.total_price}"


class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to="csvs", null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
