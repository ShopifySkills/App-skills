# Segmentation Playbook

Reusable frameworks for building and activating e-commerce customer segments.

---

## RFM scoring methodology

### Step 1: Calculate raw values per customer

| Metric | Calculation |
|--------|------------|
| Recency | Days since last order (lower = better) |
| Frequency | Total order count (higher = better) |
| Monetary | Total spend in $ (higher = better) |

### Step 2: Assign quintile scores (1–5)

Sort customers by each metric and divide into 5 equal groups. Assign score 5 to the best quintile, 1 to the worst.

For Recency, "best" = most recent (fewest days). For Frequency and Monetary, "best" = highest value.

### Step 3: Map to segments

Use the combined RFM score to assign segments. Common mappings:

| RFM range | Segment name | Description |
|-----------|-------------|-------------|
| R=5, F=5, M=5 | Champions | Recent, frequent, high-value |
| R≥4, F≥4, M≥4 | Loyal | Consistent high-value buyers |
| R≥4, F=2–3, M=2–3 | Potential Loyalists | Recent, growing engagement |
| R=5, F=1, M=1–2 | New | Just bought, first timer |
| R=3, F=3–4, M=3–4 | Needs Attention | Decent history, slowing down |
| R=2, F=3–4, M=3–4 | At-Risk | Formerly active, going quiet |
| R=1–2, F=4–5, M=4–5 | Can't Lose Them | Were champions, now lapsed |
| R=1, F=1–2, M=1–2 | Hibernating | Long gone, low value |

These thresholds are starting points. Adjust based on the store's data distribution.

---

## Lifecycle stage thresholds by category

Different products have different natural repurchase cycles. Use these as defaults and adjust:

| Category | Active (days) | At-Risk (days) | Lapsed (days) | Churned (days) |
|----------|-------------:|---------------:|--------------:|--------------:|
| Beauty / skincare | < 60 | 60–120 | 120–270 | 270+ |
| Fashion / apparel | < 90 | 90–180 | 180–365 | 365+ |
| Food / beverage / consumables | < 30 | 30–60 | 60–120 | 120+ |
| Electronics / tech | < 180 | 180–365 | 365–730 | 730+ |
| Home / furniture | < 180 | 180–365 | 365–730 | 730+ |
| Pet supplies | < 45 | 45–90 | 90–180 | 180+ |
| Supplements / vitamins | < 30 | 30–60 | 60–120 | 120+ |

Ask the merchant: "How often does a happy customer reorder?" and calibrate from there.

---

## Email tactic templates by segment

### New customers — Welcome series (3–5 emails over 14 days)

1. **Welcome + brand story** (Day 0) — introduce the brand, set expectations, no hard sell
2. **Product education** (Day 3) — how to use, tips, ingredients/materials
3. **Social proof** (Day 7) — reviews, UGC, community
4. **Second purchase nudge** (Day 10) — complementary product rec + incentive
5. **Review ask** (Day 14) — ask for feedback on first purchase

### At-Risk — Win-back flow (3 emails over 21 days)

1. **Soft nudge** (Day 0) — "It's been a while" + bestsellers or new arrivals
2. **Incentive** (Day 7) — 15–20% off or free shipping, clear deadline
3. **Last chance** (Day 14) — urgency + "We don't want to lose you" + feedback ask

### Champions — VIP treatment (ongoing)

- Early access to new drops (24–48 hours before general release)
- Surprise gift on 5th or 10th order
- Referral program with meaningful reward (not just $5)
- Annual "thank you" note (personal tone, not templated)
- Priority support flag in helpdesk

### Hibernating — Sunset flow (2 emails)

1. **Final offer** — deep discount or exclusive; clear "last email" language
2. **Unsubscribe or confirm** — "Want to keep hearing from us?" Re-engage or clean the list

---

## Pareto analysis (80/20) guide

### How to run it
1. Sort customers by total revenue (descending)
2. Calculate cumulative revenue %
3. Find the cutoff where cumulative = 80%
4. Count how many customers that covers → that's your "vital few"

### What to do with it
- **Top 20%**: These customers fund your business. Protect them with VIP treatment, personal outreach, and retention-first tactics. Never let them churn without a fight.
- **Middle 60%**: Growth opportunity. Move them toward the top with cross-sell, frequency nudges, and loyalty programs.
- **Bottom 20%**: Not all customers are worth equal effort. Suppress from expensive channels (SMS, paid retargeting). Focus on low-cost email.

---

## Product affinity analysis

### Method: Co-purchase matrix

For each pair of products (A, B), count how many customers bought both. Then calculate:

```
affinity_score = customers_who_bought_A_and_B / customers_who_bought_A
```

High affinity (>25%) = strong cross-sell signal.

### Common affinity patterns by category

| Category | Common affinity pairs |
|----------|----------------------|
| Beauty | Cleanser → Serum → Moisturizer (routine building) |
| Fashion | Top → Bottom (outfit completing); Core → Accessories |
| Food | Sampler → Full-size; Base → Add-on flavors |
| Pet | Food → Treats → Supplements (trust ladder) |
| Electronics | Device → Accessories → Replacement parts |

### How to activate
- **Email**: "Complete your routine" / "Complete the look" with the high-affinity product
- **PDP**: "Frequently bought together" widget
- **Cart**: Bundle suggestion at checkout
- **Post-purchase**: Cross-sell in order confirmation or Day 7 follow-up

---

## Segment size benchmarks

Healthy segment distribution for a mature DTC brand:

| Segment | Healthy range | Red flag |
|---------|-------------:|----------|
| Champions | 5–10% | < 3% (too few loyal buyers) |
| Loyal | 10–15% | < 5% (retention problem) |
| New | 15–25% | > 40% (too acquisition-dependent) |
| At-Risk | 10–15% | > 25% (retention leak) |
| Churned/Hibernating | 15–25% | > 40% (customer base is dying) |

If New > Churned by a wide margin, the brand is growing. If Churned > New, the brand is shrinking despite what revenue might show.

---

## Monthly segmentation review checklist

- [ ] Refresh RFM scores (recalculate monthly)
- [ ] Check segment migration (who moved from Active → At-Risk?)
- [ ] Review VIP list — any new Champions? Any Champions slipping?
- [ ] Check win-back flow performance (reactivation rate)
- [ ] Review new-customer second-purchase rate
- [ ] Update product affinity matrix if catalog changed
- [ ] Compare segment sizes to benchmarks above
- [ ] Suppress Hibernating from paid channels
