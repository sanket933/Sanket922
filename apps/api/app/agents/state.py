from typing import Any, TypedDict


class CompanyOSState(TypedDict, total=False):
    workspace_id: str
    business_context: dict[str, Any]
    trends: list[dict[str, Any]]
    content_ideas: list[dict[str, Any]]
    content_variants: list[dict[str, Any]]
    reel_jobs: list[dict[str, Any]]
    leads: list[dict[str, Any]]
    outreach: list[dict[str, Any]]
    proposed_actions: list[dict[str, Any]]
    ceo_decisions: list[dict[str, Any]]
    ops_decisions: list[dict[str, Any]]
    metrics: dict[str, Any]
