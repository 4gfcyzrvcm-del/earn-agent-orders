# Earn Agent — autonomous growth specification v2.0

**Status:** implementation started, not fully operational. **Owner:** project operator. **Date:** 2026-10-20.

## Mission
Generate **verified net profit** by finding lawful customers, proposing fixed-scope digital services, completing accepted work, and safely receiving payment. Separately test new product ideas and improve sales conversion. Never report inquiries as sales or unverified transactions as revenue.

## Agent roles
- **Coordinator:** prioritize work using actual conversion, quality and net profit; enforce limits.
- **Research:** identify demand, competitors, and suitable funded opportunities with original source URLs.
- **Sales:** qualify inbound leads, draft tailored quotes, record acceptance criteria; no unsolicited bulk messaging.
- **Marketing:** publish accurate service pages, SEO content and case studies; no fake testimonials or engagement.
- **Product:** propose, prototype and test new services based on evidence.
- **Developer/QA:** implement tasks in isolated branches; run tests; inspect outputs before delivery.
- **Finance:** match verified transactions to orders, fees and expenses; report profit and exceptions.

## End-to-end order lifecycle
`lead -> qualified -> quoted -> accepted -> awaiting_payment -> paid_verified -> in_progress -> QA -> delivered -> closed`.
Allow `rejected`, `cancelled`, `disputed`, and `refunded` states. Never mark paid from customer-submitted screenshots or a reused TXID.

Every order must store a stable order ID, customer contact channel, scope, deliverables, acceptance tests, agreed price/currency, deadlines, quote/acceptance evidence, payment identifiers, expenses and audit events. Do not put customer secrets or private datasets in public GitHub issues.

## Autonomous growth loop
1. Find opportunities through permitted channels and check current availability, clear budget, scope, payout and platform rules.
2. Rank by expected net return, feasibility, competition and risk.
3. Draft personalized offers only where outreach is permitted and avoid repetitive spam.
4. Record outcomes and refine service descriptions and pricing.
5. Generate **draft** new service pages and prototypes, test them, and publish only under approved release rules.
6. Measure leads, conversion, paid orders, refunds, delivery quality, expenses and net profit.
7. Pause failing or unprofitable experiments; preserve reproducible audit logs.

## Guardrails
- No autonomous spending, binding contracts, wallet changes, funds transfer, bulk unsolicited messages, account creation, or irreversible deployment without owner-approved policy or explicit consent.
- Never evade platform restrictions, sanctions, KYC/AML or tax requirements.
- Read-only chain verification requires the correct USDT TRC20 contract, destination, amount, confirmed status and **unique TXID allocation to exactly one order**. No key custody.
- Secure secrets server-side, use least-privilege tokens, data minimization, rate limits, rollback, and manual escalation.
- GitHub Actions alone is not a continuously running business server.

## Existing components (not equivalent to completion)
- GitHub Pages landing page and GitHub issue intake.
- Auto-generated indicative issue quote; scope/acceptance still manual.
- Prototype TRC20 checker with offline tests; **not proven on a real payment**.
- Daily discovery automation; no confirmed customers or revenue.

## Implementation roadmap and acceptance gates
**P0 — first paid order:** improve conversion-oriented landing page; intake with explicit task examples and safe scope; establish permitted client outreach; record qualified leads; confirm payment and delivery manually if necessary. Gate: one real customer, agreed scope, confirmed payment and delivered result.

**P1 — reliable order processing:** persistent order ledger, payment TXID uniqueness and confirmations, QA/delivery queue, refund/dispute handling, owner dashboard. Gate: automated tests + real verified end-to-end transaction.

**P2 — product creation:** propose and build new service prototypes in branches, compare expected margin and demand, deploy through approved review. Gate: tested product with real demand evidence.

**P3 — continuous optimization:** scheduled experiments, marketing attribution, monitored ROI, secure deployment, alerts and rollback. Gate: positive repeatable net profit, not merely website traffic.

## Current financial baseline
Confirmed paid orders: **0**. Verified revenue: **0 USDT**. No promise of future earnings.
