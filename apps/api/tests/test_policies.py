from app.agents.policies import validate_action_batch
from app.models.schemas import ActionType, ProposedAction


def test_outreach_limit_blocks_large_email_batch():
    actions = [ProposedAction(workspace_id='w1', action_type=ActionType.email_send, target=f'lead-{i}', payload={'body': 'hello'}, rationale='test') for i in range(31)]
    decisions = validate_action_batch(actions)
    assert any(not d['approved'] and d['reason'] == 'outreach_daily_limit_exceeded' for d in decisions)


def test_platform_limit_blocks_excess_linkedin_posts():
    actions = [ProposedAction(workspace_id='w1', action_type=ActionType.social_post, platform='linkedin', payload={'body': 'post'}, rationale='test') for _ in range(4)]
    decisions = validate_action_batch(actions)
    assert any(not d['approved'] and d['reason'] == 'platform_daily_limit_exceeded' for d in decisions)
