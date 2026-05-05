# Production Architecture Blueprint

## Queue Architecture

- `daily_company_cycle`: Celery task that runs the LangGraph company graph.
- `approval_dispatch`: future-safe queue for Make.com/social/email dispatch after CEO + Operations approval.
- `analytics_ingest`: provider analytics and IMAP reply ingestion.
- `media_render`: FFmpeg reel rendering and subtitle burn-in jobs.

Redis is the broker/result backend locally and should be upgraded to managed Redis in production. Workers use late acknowledgements and retry backoff to avoid losing jobs during deploys or transient API failures.

## Agent Workflows

### CEO Agent

The CEO agent initializes business context, sets the approval policy, and validates whether proposed actions support growth goals. No external action can execute until the CEO decision is positive.

### Marketing Agent

The Marketing agent converts trend and competitor intelligence into platform-aware ideas for LinkedIn, Instagram, and X/Twitter. In production, replace or extend its data collectors with approved APIs, RSS feeds, social analytics exports, and SERP providers.

### Content Developer Agent

The Content agent transforms each idea into unique platform variants instead of reposting identical copy. LinkedIn receives authority-led posts, Instagram receives retention-first reels, and X receives concise opinionated threads.

### Sales Agent

The Sales agent analyzes lead pain points and creates personalized cold outreach drafts. Sending remains gated by CEO approval, Operations safety validation, and optional human review.

### Operations Agent

The Operations agent enforces platform rate limits, anti-spam rules, duplicate-contact checks, queue health, and risk scoring. High-risk actions are paused and routed to review.

## API Integrations

- OpenAI: reasoning, copy generation, embeddings, image/video prompts.
- LangSmith: trace agent runs, monitor quality, debug regressions.
- LinkedIn API: approved UGC, image, and video publishing through Make.com or backend connector.
- Meta Graph / Instagram Business API: reels, carousels, captions, and analytics.
- X API: tweets, threads, and analytics.
- YouTube API: Shorts uploads and performance metrics.
- Replicate / Stability AI: optional visual and video generation providers.
- Hostinger SMTP/IMAP: cold email sending and reply ingestion without Gmail OAuth.

## Reel Generation Workflow

1. Marketing agent selects trend and retention angle.
2. Content agent writes hook, script, CTA, and scene list.
3. Media service creates a manifest for 9:16 output.
4. Image/video providers generate source assets.
5. FFmpeg normalizes visuals to 1080x1920, overlays subtitles, adds transitions and optional voiceover.
6. Operations agent validates platform limits and duplicate-risk.
7. Make.com uploads approved versions to Instagram, LinkedIn, YouTube Shorts, or Facebook.

## Approval System

Every external action becomes an `approval_items` row. The lifecycle is `pending -> ceo_approved -> ops_approved -> human_required|dispatched|rejected`. Human review can be required per workspace, campaign, platform, or risk score.

## Security Architecture

- Backend-only secrets via `.env`, Railway secrets, Vercel secrets, or Make vault.
- No SMTP, IMAP, OAuth, or AI provider tokens are exposed to the frontend.
- Webhooks use timestamped HMAC verification.
- Rate limiting is enforced at FastAPI ingress.
- Audit logs store every approval, dispatch, webhook, retry, and provider response.
- Database rows are scoped by workspace and ready for Supabase RLS policies.

## Anti-Ban and Deliverability System

- Per-platform daily publishing limits.
- Per-target duplicate outreach checks.
- Spam phrase and risk scoring before dispatch.
- Warm-up plan: begin with low email volume, gradually scale only after healthy replies and low bounces.
- DNS requirements: SPF, DKIM, and DMARC (`v=DMARC1; p=quarantine; pct=100;`).

## CRM and Memory Architecture

- `leads`: company identity, pain points, score, status.
- `conversations`: email/DM history and reply tracking.
- `content_assets`: content and media lifecycle.
- `analytics_events`: platform performance events.
- `memories`: pgvector embeddings for reusable business, content, lead, and analytics memory.
- `audit_logs`: immutable operational trace.

## Deployment Strategy

- Vercel: Next.js web console.
- Railway/Render: FastAPI API and Celery workers.
- Supabase: Postgres, auth integration, pgvector memory.
- Managed Redis: queue broker and result backend.
- Object storage: generated reels, carousels, thumbnails, subtitles, and exports.

## Monitoring Strategy

- `/health` endpoint for uptime checks.
- LangSmith for agent traces and LLM observability.
- Celery metrics for queue depth, failures, retries, and latency.
- Audit logs for compliance and debugging.
- Provider response IDs stored for social/email traceability.

## Scalability Plan

- Split workers by queue: `agents`, `media`, `dispatch`, `analytics`.
- Autoscale media workers separately because FFmpeg and video generation are CPU/GPU intensive.
- Use idempotency keys on approval dispatches to prevent duplicate posts or emails.
- Partition analytics events by time/workspace as volume grows.
- Move long-term media to object storage with signed URLs.
