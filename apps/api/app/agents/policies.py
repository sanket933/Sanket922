from collections import Counter
from app.models.schemas import ProposedAction


PLATFORM_DAILY_LIMITS = {'linkedin': 3, 'instagram': 3, 'x': 8, 'facebook': 2, 'youtube': 2}
OUTREACH_DAILY_LIMIT = 30


def score_spam_risk(action: ProposedAction, recent_actions: list[ProposedAction]) -> float:
    risk = action.risk_score
    same_target = sum(1 for item in recent_actions if item.target == action.target and action.target)
    if same_target:
        risk += min(0.4, same_target * 0.2)
    if action.action_type.value in {'email_send', 'dm_send'}:
        body = str(action.payload).lower()
        spam_terms = ['guaranteed', 'free money', 'act now', 'limited time']
        risk += min(0.3, sum(term in body for term in spam_terms) * 0.1)
    return min(1.0, risk)


def validate_action_batch(actions: list[ProposedAction]) -> list[dict]:
    platform_counts = Counter(a.platform for a in actions if a.platform)
    email_count = sum(1 for a in actions if a.action_type.value == 'email_send')
    decisions = []
    for action in actions:
        reason = 'safe_to_execute'
        approved = True
        if action.platform and platform_counts[action.platform] > PLATFORM_DAILY_LIMITS.get(action.platform, 1):
            approved = False
            reason = 'platform_daily_limit_exceeded'
        if action.action_type.value == 'email_send' and email_count > OUTREACH_DAILY_LIMIT:
            approved = False
            reason = 'outreach_daily_limit_exceeded'
        if score_spam_risk(action, actions) >= 0.7:
            approved = False
            reason = 'spam_or_ban_risk_too_high'
        decisions.append({'action': action.model_dump(), 'approved': approved, 'reason': reason})
    return decisions
