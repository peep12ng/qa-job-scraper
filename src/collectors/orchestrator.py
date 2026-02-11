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
