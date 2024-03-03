from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Students)
def create_profile(sender, instance, created, **kwargs):
    if created:
        products = Products.objects.get(pk=instance.product_id)