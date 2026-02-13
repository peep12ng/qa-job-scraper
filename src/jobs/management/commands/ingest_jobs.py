from __future__ import annotations

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from collectors.core.normalization import normalize_items
from jobs.services.job_store import store_items

class Command(BaseCommand):
    help = "Ingest normalized job items from a fixture JSON file."

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)
        parser.add_argument("--source-code", dest="source_code", default=None)
        parser.add_argument(
            "--show-errors",
            action="store_true",
            dest="show_errors",
            help="Show first 20 validation/storage errors.",
        )

    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"file not found: {path}")

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(f"invalid json: {exc}") from exc

        source_code = options.get("source_code")

        if isinstance(payload, dict) and "items" in payload:
            items = payload.get("items") or []
            source_code = source_code or payload.get("source_code")
        elif isinstance(payload, list):
            items = payload
        else:
            raise CommandError("payload must be a list or an object with an 'items' key")

        normalized, errors = normalize_items(items, source_code=source_code)
        stored, skipped, store_errors = store_items(normalized)

        all_errors = errors + store_errors
        self.stdout.write(
            f"OK stored={stored} skipped={skipped} errors={len(all_errors)} normalized={len(normalized)}"
        )

        if options.get("show_errors"):
            for error in all_errors[:20]:
                self.stdout.write(self.style.WARNING(f"- {error}"))
