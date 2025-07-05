from django.apps import AppConfig
from django.db.utils import OperationalError


class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'

    def ready(self):
        # TODO: Remove this when the site is deployed, this points auth to localhost:8000
        from django.contrib.sites.models import Site
        try:
            site = Site.objects.get(id=1)
            site.domain = 'localhost:8000'
            site.name = 'Quiz of Fury'
            site.save()
        except OperationalError:
            # Ignore safely for now
            pass