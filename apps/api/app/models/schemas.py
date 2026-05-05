from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from typing import Any


class ActionType(str, Enum):
    social_post = 'social_post'
    reel_publish = 'reel_publish'
    email_send = 'email_send'
    dm_send = 'dm_send'
    lead_research = 'lead_research'
    analytics_sync = 'analytics_sync'


class ApprovalStatus(str, Enum):
    pending = 'pending'
    ceo_approved = 'ceo_approved'
    ops_approved = 'ops_approved'
    human_required = 'human_required'
    rejected = 'rejected'
    dispatched = 'dispatched'


class ProposedAction(BaseModel):
    workspace_id: str
    action_type: ActionType
    platform: str | None = None
    target: str | None = None
    payload: dict[str, Any]
    risk_score: float = Field(ge=0, le=1, default=0)
    rationale: str


class LeadResearchRequest(BaseModel):
    workspace_id: str
    company_name: str
    website: HttpUrl | None = None
    social_url: HttpUrl | None = None


class DailyRunRequest(BaseModel):
    workspace_id: str
    human_approval_required: bool = True
    max_posts_per_platform: int = 2
    max_outreach_emails: int = 20
