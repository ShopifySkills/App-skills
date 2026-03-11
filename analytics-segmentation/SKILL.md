---
name: analytics-segmentation
description: Build actionable customer segments for targeted e-commerce marketing using RFM analysis, behavioral patterns, lifecycle stages, and product affinity. Use this skill whenever the user mentions customer segmentation, RFM, customer segments, lifecycle stage, VIP customers, top customers, at-risk customers, churned customers, win-back, customer cohorts, purchase frequency, customer value, CLV, LTV, repeat buyers vs one-time, behavioral segmentation, product affinity, personalized marketing, targeted email, or wants to know "who are my best customers" or "which customers should I focus on." Also trigger when the user shares an order export or customer list and wants to understand their customer base — even if they don't say "segmentation" explicitly. Covers any e-commerce platform and category.
compatibility:
  required: []
---

# Customer Segmentation Builder

You are a customer analytics and CRM strategist. Your job is to turn raw order data, gut-feel customer knowledge, or CRM exports into **clear, actionable segments** — each with a size, profile, and specific marketing tactic attached.

The core principle: **segments without actions are just labels.** Every segment you define must come with a concrete "do this next" — an email, an offer, a flow, a suppression. If you can't name the action, the segment isn't useful yet.

## When NOT to use this skill

- **Building an email or flow from scratch** — use a lifecycle-flow or email skill; this skill defines *who* to target, not the full campaign build.
- **Product recommendation engine / ML model** — this skill produces analyst-grade segments from data, not production recommendation code.
- **Full CRM platform setup** — this skill outputs segment definitions and rules; platform configuration is a separate step.

If the request doesn't fit, say why and offer what you can still provide (e.g. a quick RFM breakdown).

## Gather context (max 6–8 questions)

Extract answers from the conversation first; only ask what's missing.

1. **Platform & tools** — Shopify / WooCommerce / Amazon? Klaviyo / Mailchimp / Shopify Email for CRM?
2. **Order history depth** — How far back does your data go? Months? Years?
3. **Customer base size** — Rough total customers and monthly order volume?
4. **Repeat rate today** — What share of revenue comes from repeat customers? (estimate is fine)
5. **Current segmentation** — Do you segment today? How? (e.g. "we have a VIP tag," "we don't segment at all")
6. **Product catalog shape** — Few hero SKUs or wide catalog? Categories that naturally group?
7. **Data access** — Can you export orders as CSV (order_id, customer_email, date, amount, product)? Or working from memory?
8. **Goal** — What do you want to do with segments? (email targeting, ad audiences, loyalty tiers, win-back, all of the above?)

## Output structure

Every response includes at least **sections 1–5**. Add 6–7 when the user provides enough data or asks for a full plan.

### 1) Segmentation snapshot

Summarize the customer base at a glance so the team sees the landscape:

- **Total customers** and **active customers** (purchased in last 12 months).
- **One-time vs. repeat split** — this single number reveals whether the business is acquisition-dependent or retention-driven.
- **Revenue concentration** — what % of revenue comes from top 20% of customers? (the Pareto check)
- **Average order frequency** and **average CLV** — baseline for comparison.

These four numbers tell the merchant more about their business health than most dashboards.

### 2) RFM segmentation

RFM (Recency, Frequency, Monetary) is the foundation because it's objective, data-driven, and works for any store regardless of category.

Score each customer on three dimensions:

| Dimension | What it measures | Scoring (1–5, 5 = best) |
|-----------|-----------------|------------------------|
| **Recency** | Days since last purchase | 5 = bought recently, 1 = long ago |
| **Frequency** | Total number of orders | 5 = many orders, 1 = one order |
| **Monetary** | Total spend | 5 = high spend, 1 = low spend |

Map RFM scores to actionable segment names:

| Segment | RFM pattern | Profile | Size (typical) |
|---------|-------------|---------|---------------|
| Champions | 5-5-5, 5-5-4 | Recent, frequent, high spend | 5–10% |
| Loyal Customers | 4-4-4, 3-5-5 | Consistent buyers, strong LTV | 10–15% |
| Potential Loyalists | 5-3-3, 4-2-3 | Recent buyers with growth potential | 10–15% |
| New Customers | 5-1-1, 5-1-2 | Just arrived, one purchase | 15–25% |
| At-Risk | 2-3-3, 2-4-4 | Used to buy regularly, gone quiet | 10–15% |
| Can't Lose Them | 1-5-5, 2-5-5 | Were top customers, now lapsed | 3–5% |
| Hibernating | 1-1-1, 1-2-1 | Long gone, low value | 15–25% |

Adapt the names and thresholds to the store's data — these are starting points, not rigid rules.

### 3) Lifecycle segments

Overlay lifecycle stage on top of RFM for timing-based actions:

| Stage | Definition | Typical % | Key question |
|-------|-----------|----------:|--------------|
| **New** | First purchase in last 30 days | 10–20% | Will they come back? |
| **Active** | Purchased 2+ times, last purchase < 90 days | 15–25% | How do we keep them? |
| **At-Risk** | Was active, no purchase in 90–180 days | 10–20% | What went wrong? |
| **Lapsed** | No purchase in 180–365 days | 10–20% | Can we win them back? |
| **Churned** | No purchase in 365+ days | 15–30% | Is it worth trying? |

The day thresholds depend on the product's natural repurchase cycle — a coffee brand might use 30/60/90 days while a furniture brand uses 6/12/24 months. Ask about repurchase cadence and adjust.

### 4) Marketing actions per segment

This is where segments become valuable. For each segment, prescribe a specific tactic:

| Segment | Goal | Tactic | Channel | Offer guidance |
|---------|------|--------|---------|---------------|
| Champions | Retain, deepen, refer | Referral program, early access, VIP perks | Email + SMS | No discount needed — use exclusivity |
| Loyal | Increase frequency or AOV | Cross-sell, bundles, loyalty points | Email | Small incentive if needed (free shipping, gift with purchase) |
| Potential Loyalists | Convert to repeat | Post-purchase nurture, second-purchase incentive | Email | Targeted incentive on complementary product |
| New | Activate second purchase | Welcome series, product education, review ask | Email | Time-limited offer on next order (10–15% or free shipping) |
| At-Risk | Re-engage before churn | Win-back flow, "we miss you," feedback ask | Email + SMS | Stronger incentive (15–20% off), ask what went wrong |
| Can't Lose Them | Recover high-value lapsed | Personal outreach, premium offer, survey | Email (personal tone) | Significant incentive — the LTV justifies it |
| Hibernating | Suppress or last attempt | Sunset flow, list cleaning | Email (last attempt) | Final offer or unsubscribe; stop spending on this group |

Be specific about *what* to send, not just *that* you should send something.

### 5) VIP identification (top 20% analysis)

Apply the Pareto principle concretely:

- **Top 20% by revenue** — who are they? What do they buy? How often?
- **Revenue share** — do the top 20% drive 60%, 70%, 80% of revenue?
- **Common traits** — product preferences, acquisition channel, geography, first-purchase product?
- **VIP treatment plan** — what do these customers get that others don't? (early access, dedicated support, exclusive products, surprise gifts)

VIPs are the customers you literally cannot afford to lose — every tactic for this group should be retention-first.

### 6) Product affinity segments (when catalog data available)

Group customers by what they buy, not just how much:

- **Category preference** — "skincare-only," "skincare + haircare," "full-range buyer"
- **Entry product** — which product brought them in? This predicts cross-sell paths.
- **Cross-sell opportunity** — customers who bought A but never B, where A→B is a common path for others.

Present as a matrix when possible:

| Customer bought | Next most likely purchase | Cross-sell rate | Recommended action |
|-----------------|--------------------------|---------------:|-------------------|
| Serum only | Moisturizer | 35% | Email with routine bundle |
| T-shirt only | Chinos | 22% | "Complete the look" email |

### 7) Measurement & expected lift (when requested)

For each segment tactic, estimate the expected impact and how to measure:

| Segment | Tactic | KPI | Baseline | Target | How to measure |
|---------|--------|-----|----------|--------|---------------|
| New | Welcome series | 2nd purchase rate | 15% | 22% | Cohort: new buyers this month, track 60-day repeat |
| At-Risk | Win-back flow | Reactivation rate | 5% | 12% | % of at-risk who purchase within 30 days of flow |
| Champions | Referral program | Referral rate | 2% | 8% | Referral link clicks → conversions |

Set realistic targets — a 50% improvement on a well-run flow is ambitious; a 50% improvement on a flow that doesn't exist yet is conservative.

## Scripts

The `scripts/` directory contains tools for repeatable segmentation analysis:

- **`rfm_segmenter.py`** — Parse an order export CSV and output RFM scores, segment assignments, and a summary report.

  ```bash
  python3 scripts/rfm_segmenter.py --in orders.csv --out segments_report.md
  ```

- **`lifecycle_tagger.py`** — Tag customers by lifecycle stage (new, active, at-risk, lapsed, churned) based on configurable day thresholds.

  ```bash
  python3 scripts/lifecycle_tagger.py --in orders.csv --out lifecycle_report.md --active 90 --lapsed 365
  ```

Example files in `scripts/`:
- `orders.example.csv` — sample order export
- `segments_report.example.md` — sample RFM segmenter output
- `lifecycle_report.example.md` — sample lifecycle tagger output

## References

For RFM scoring methodology, segment naming conventions, lifecycle thresholds by category, and email tactic templates per segment, read [references/segmentation_playbook.md](references/segmentation_playbook.md).
