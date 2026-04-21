from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Person


@receiver(post_save, sender=Person)
def handle_wanted_change(sender, instance, **kwargs):
    from recognition.surveillance import manager

    if instance.is_wanted:
        if not manager.is_running:
            manager.start()
        # if already running, threads reload wanted persons every 30s automatically
    else:
        if not Person.objects.filter(is_wanted=True).exists():
            manager.stop()
