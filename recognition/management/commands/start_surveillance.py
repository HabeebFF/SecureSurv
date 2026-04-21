import time
from django.core.management.base import BaseCommand
from recognition.surveillance import manager


class Command(BaseCommand):
    help = "Manually start surveillance (normally auto-starts via signals)."

    def handle(self, *args, **kwargs):
        manager.start()
        if not manager.is_running:
            self.stdout.write(self.style.ERROR("No active cameras found."))
            return
        self.stdout.write(self.style.SUCCESS("Surveillance running. Press Ctrl+C to stop."))
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop()
