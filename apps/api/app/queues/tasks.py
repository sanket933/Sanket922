from app.agents.graph import build_company_graph
from app.queues.celery_app import celery_app


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def run_daily_company_cycle(self, workspace_id: str) -> dict:
    graph = build_company_graph()
    return graph.invoke({'workspace_id': workspace_id})
