from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Sale

@receiver(m2m_changed, sender=Sale.positions.through)
def calculate_total_price(sender, instance, action, **kwargs):
    total = 0
    if action == "post_add" or action == "post_remove":
        for item in instance.get_positions():
            total += item.price

    instance.total_price = total
    instance.save()