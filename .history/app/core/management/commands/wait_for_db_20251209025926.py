"""
Django command to wait for the database to be available.
"""

import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for the database."""

    def check(self, databases=None):
        """Override check to allow patching in tests."""
        return super().check(databases=databases)

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_ready = False

        while db_ready is False:
            try:
                self.check(databases=['default'])
                db_ready = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
