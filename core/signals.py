from django.db.models.signals import pre_delete
from django.dispatch import receiver
from core.models import Review
import logging


@receiver(pre_delete, sender=Review)
def delete_review(sender, instance, **kwargs):
        return
