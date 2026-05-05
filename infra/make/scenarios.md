# Make.com Scenarios

Make.com is execution-only. Every scenario must accept backend-approved payloads and must never generate strategy, content, or personalization.

## Shared Requirements

- Use custom webhook trigger with HMAC headers from backend.
- Reject payloads without `approval_item_id` and `ops_approved=true`.
- Log provider response IDs back to `/api/v1/webhooks/make`.
- Retry transient provider errors with exponential backoff.

## Scenario: publish_social_post

1. Custom webhook receives approved post payload.
2. Router branches by `platform`.
3. LinkedIn module publishes UGC/image/video.
4. Meta Graph module publishes Instagram/Facebook content.
5. X API module publishes tweet/thread.
6. HTTP callback sends status and analytics seed to backend.

## Scenario: publish_reel

1. Custom webhook receives `media_url`, caption, cover, platform variants.
2. Upload video to Instagram Reels / LinkedIn video / YouTube Shorts as requested.
3. Wait for processing completion where provider supports it.
4. Callback backend with permalink and provider media ID.

## Scenario: send_hostinger_email

1. Custom webhook receives approved outreach payload.
2. SMTP module uses `smtp.hostinger.com:465` with SSL/TLS and backend-only Make secret vault credentials.
3. Send personalized message from `info@therisewebd.in`.
4. Callback backend with message ID and delivery status.

## Scenario: watch_hostinger_replies

1. IMAP module watches `imap.hostinger.com:993` with SSL.
2. New replies are sent to backend webhook.
3. Backend updates CRM, memory, and follow-up state.
