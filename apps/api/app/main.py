from fastapi import FastAPI, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.agents.graph import build_company_graph
from app.core.security import verified_webhook
from app.models.schemas import DailyRunRequest, LeadResearchRequest
from app.queues.tasks import run_daily_company_cycle

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title='Autonomous AI Company OS', version='0.1.0')
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.get('/health')
def health() -> dict:
    return {'status': 'ok'}


@app.post('/api/v1/runs/daily')
@limiter.limit('10/minute')
def start_daily_run(request: Request, payload: DailyRunRequest) -> dict:
    task = run_daily_company_cycle.delay(payload.workspace_id)
    return {'task_id': task.id, 'status': 'queued'}


@app.post('/api/v1/runs/daily/preview')
@limiter.limit('5/minute')
def preview_daily_run(request: Request, payload: DailyRunRequest) -> dict:
    graph = build_company_graph()
    return graph.invoke({'workspace_id': payload.workspace_id})


@app.post('/api/v1/leads/research')
@limiter.limit('30/minute')
def research_lead(request: Request, payload: LeadResearchRequest) -> dict:
    return {'workspace_id': payload.workspace_id, 'lead': payload.model_dump(), 'status': 'queued_for_sales_agent'}


@app.post('/api/v1/webhooks/make')
async def receive_make_webhook(raw_body: bytes = Depends(verified_webhook)) -> dict:
    return {'received': True, 'bytes': len(raw_body)}
