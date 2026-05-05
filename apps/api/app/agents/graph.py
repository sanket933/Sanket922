from langgraph.graph import END, StateGraph
from app.agents.state import CompanyOSState
from app.agents.policies import validate_action_batch
from app.models.schemas import ActionType, ProposedAction


def ceo_agent(state: CompanyOSState) -> CompanyOSState:
    state['business_context'] = {
        'goal': 'grow authority, pipeline, and conversions for AI/web services',
        'approval_policy': 'CEO approval required before all external actions',
    }
    return state


def marketing_agent(state: CompanyOSState) -> CompanyOSState:
    state['trends'] = [
        {'topic': 'AI automation for small businesses', 'platforms': ['linkedin', 'instagram', 'x'], 'confidence': 0.82},
        {'topic': 'Founder-led growth systems', 'platforms': ['linkedin', 'x'], 'confidence': 0.76},
    ]
    state['content_ideas'] = [
        {'idea': 'Why service businesses need an AI operating system', 'angle': 'authority'},
        {'idea': 'Three automations that save founders 10 hours weekly', 'angle': 'tactical'},
    ]
    return state


def content_agent(state: CompanyOSState) -> CompanyOSState:
    variants = []
    for idea in state.get('content_ideas', []):
        variants.extend([
            {'platform': 'linkedin', 'format': 'post', 'hook': f"Most founders misunderstand {idea['idea'].lower()}.", 'cta': 'Comment OPERATING SYSTEM for the checklist.'},
            {'platform': 'instagram', 'format': 'reel', 'hook': f"Stop wasting hours: {idea['idea'].lower()}.", 'cta': 'Save this before you automate.'},
            {'platform': 'x', 'format': 'thread', 'hook': f"Hot take: {idea['idea'].lower()} is no longer optional.", 'cta': 'Reply AIOS and I will share the stack.'},
        ])
    state['content_variants'] = variants
    state['reel_jobs'] = [v for v in variants if v['format'] == 'reel']
    return state


def sales_agent(state: CompanyOSState) -> CompanyOSState:
    state['leads'] = [
        {'company': 'Local service business', 'pain_point': 'manual lead follow-up', 'score': 0.71},
        {'company': 'B2B agency', 'pain_point': 'inconsistent content engine', 'score': 0.68},
    ]
    state['outreach'] = [
        {'target': lead['company'], 'subject': 'Quick automation idea', 'body': f"Noticed {lead['pain_point']}. I mapped a small AI workflow that could reduce the manual work without changing your current tools."}
        for lead in state['leads']
    ]
    return state


def propose_actions(state: CompanyOSState) -> CompanyOSState:
    actions: list[ProposedAction] = []
    for variant in state.get('content_variants', []):
        actions.append(ProposedAction(
            workspace_id=state['workspace_id'],
            action_type=ActionType.reel_publish if variant['format'] == 'reel' else ActionType.social_post,
            platform=variant['platform'],
            payload=variant,
            rationale='Platform-specific content generated from approved trend intelligence.',
        ))
    for item in state.get('outreach', []):
        actions.append(ProposedAction(
            workspace_id=state['workspace_id'],
            action_type=ActionType.email_send,
            target=item['target'],
            payload=item,
            risk_score=0.25,
            rationale='Personalized lead outreach based on detected operational pain point.',
        ))
    state['proposed_actions'] = [a.model_dump() for a in actions]
    state['ceo_decisions'] = [{'action': a.model_dump(), 'approved': True, 'reason': 'aligned_with_growth_strategy'} for a in actions]
    return state


def operations_agent(state: CompanyOSState) -> CompanyOSState:
    approved = [ProposedAction(**d['action']) for d in state.get('ceo_decisions', []) if d['approved']]
    state['ops_decisions'] = validate_action_batch(approved)
    return state


def build_company_graph():
    graph = StateGraph(CompanyOSState)
    graph.add_node('ceo', ceo_agent)
    graph.add_node('marketing', marketing_agent)
    graph.add_node('content', content_agent)
    graph.add_node('sales', sales_agent)
    graph.add_node('propose', propose_actions)
    graph.add_node('operations', operations_agent)
    graph.set_entry_point('ceo')
    graph.add_edge('ceo', 'marketing')
    graph.add_edge('marketing', 'content')
    graph.add_edge('content', 'sales')
    graph.add_edge('sales', 'propose')
    graph.add_edge('propose', 'operations')
    graph.add_edge('operations', END)
    return graph.compile()
