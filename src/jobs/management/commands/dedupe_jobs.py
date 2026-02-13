from __future__ import annotations

from django.core.management.base import BaseCommand

from jobs.services.duplicate_service import dedupe_jobs

class Command(BaseCommand):
    help = "Group duplicate job posts by normalized (company/title/location) key."

    def handle(self, *args, **options):
        summary = dedupe_jobs()
        self.stdout.write(
            "OK total_jobs={total_jobs} grouped_jobs={grouped_jobs} groups_created={groups_created}".format(
                **summary
            )
        )
