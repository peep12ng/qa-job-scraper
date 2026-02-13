from typing import Callable, Dict, List, Any

from .registry import SourceSpec, get_sources

CollectorFn = Callable[[SourceSpec], Any]

def run_priority_pipeline(
    collectors: Dict[str, CollectorFn], active_only: bool = True
    ) -> List[Any]:
    results: List[Any] = []
    for source in get_sources(active_only=active_only):
        collector = collectors.get(source.code)
        if collector is None:
            continue
        results.append(collector(source))
    return results

def list_source_order(active_only: bool = True) -> List[str]:
    return [s.code for s in get_sources(active_only=active_only)]

def run_priority_pipeline_and_store(
    collectors: Dict[str, CollectorFn], active_only: bool = True
) -> List[Dict[str, int]]:
    from collectors.normalization import normalize_items
    from jobs.services.job_store import store_items

    summaries: List[Dict[str, int]] = []

    for source in get_sources(active_only=active_only):
        collector = collectors.get(source.code)
        if collector is None:
            continue

        raw_items = collector(source)
        items: List[Dict[str, Any]] = []
        if isinstance(raw_items, dict) and isinstance(raw_items.get("items"), list):
            items = raw_items.get("items") or []
        elif isinstance(raw_items, list):
            items = raw_items

        normalized, errors = normalize_items(items, source_code=source.code)
        stored, skipped, store_errors = store_items(normalized)

        summaries.append(
            {
                "source_code": source.code,
                "stored": stored,
                "skipped": skipped,
                "errors": len(errors) + len(store_errors),
            }
        )

    return summaries
