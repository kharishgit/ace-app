##
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Branch

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Branch)
def log_branch_update(sender, instance, created, **kwargs):
    if created:
        message = f'Branch "{instance.name}" created by {instance.created_by} at {instance.created_at}.'
        logger.info(message)
    else:
        message = f'Branch "{instance.name}" updated by {instance.updated_by} at {instance.updated_at}.'
        logger.info(message)

@receiver(post_delete, sender=Branch)
def log_branch_delete(sender, instance, **kwargs):
    message = f'Branch "{instance.name}" deleted by {instance.updated_by} at {instance.updated_at}.'
    logger.info(message)


