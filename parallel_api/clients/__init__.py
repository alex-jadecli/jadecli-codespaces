# ---
# entity_id: module-parallel-clients
# entity_name: Parallel.ai Clients Package
# entity_type_id: module
# entity_path: parallel_api/clients/__init__.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [ParallelClient]
# entity_dependencies: [async_client]
# entity_callers: [parallel_api]
# entity_callees: []
# entity_semver_impact: minor
# ---

"""
HTTP clients for Parallel.ai API.

Provides async and sync clients for all Parallel.ai endpoints.
"""

from parallel_api.clients.async_client import ParallelClient

__all__ = ["ParallelClient"]
