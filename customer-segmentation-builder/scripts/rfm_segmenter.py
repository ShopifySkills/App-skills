#!/usr/bin/env python3
"""
Parse an order export CSV and output RFM scores, segment assignments, and summary.

Expects columns: order_id, customer_email, order_date, amount, product.
Calculates Recency, Frequency, Monetary per customer, assigns quintile
scores 1-5, maps to named segments, and outputs a markdown report.

Usage:
    python3 scripts/rfm_segmenter.py --in orders.csv --out segments_report.md
    python3 scripts/rfm_segmenter.py --in orders.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class CustomerRFM:
    email: str
    recency_days: int
    frequency: int
    monetary: float
    r_score: int = 0
    f_score: int = 0
    m_score: int = 0
    segment: str = ""


SEGMENT_MAP: List[Tuple[str, callable]] = []


def _assign_segment(r: int, f: int, m: int) -> str:
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions" if r == 5 and f == 5 else "Loyal"
    if r >= 4 and f <= 3 and m <= 3:
        return "Potential Loyalists" if f >= 2 else "New"
    if r == 3 and f >= 3:
        return "Needs Attention"
    if r == 2 and f >= 3:
        return "At-Risk"
    if r <= 2 and f >= 4 and m >= 4:
        return "Can't Lose Them"
    if r <= 2 and f <= 2 and m <= 2:
        return "Hibernating"
    return "Others"


def _quintile_scores(values: List[float], reverse: bool = False) -> List[int]:
    indexed = sorted(enumerate(values), key=lambda x: x[1], reverse=reverse)
    n = len(indexed)
    scores = [0] * n
    for rank, (orig_idx, _) in enumerate(indexed):
        quintile = min(int(rank / n * 5) + 1, 5)
        scores[orig_idx] = quintile
    return scores


def parse_orders(path: Path, ref_date: date) -> List[CustomerRFM]:
    customers: Dict[str, Dict] = defaultdict(lambda: {"dates": [], "amounts": []})

    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            email = row["customer_email"].strip().lower()
            order_date = datetime.strptime(row["order_date"].strip(), "%Y-%m-%d").date()
            amount = float(row["amount"])
            customers[email]["dates"].append(order_date)
            customers[email]["amounts"].append(amount)

    rfm_list: List[CustomerRFM] = []
    for email, data in customers.items():
        last_date = max(data["dates"])
        rfm_list.append(CustomerRFM(
            email=email,
            recency_days=(ref_date - last_date).days,
            frequency=len(data["dates"]),
            monetary=sum(data["amounts"]),
        ))

    recencies = [c.recency_days for c in rfm_list]
    frequencies = [c.frequency for c in rfm_list]
    monetaries = [c.monetary for c in rfm_list]

    r_scores = _quintile_scores(recencies, reverse=True)
    f_scores = _quintile_scores(frequencies, reverse=False)
    m_scores = _quintile_scores(monetaries, reverse=False)

    for i, c in enumerate(rfm_list):
        c.r_score = r_scores[i]
        c.f_score = f_scores[i]
        c.m_score = m_scores[i]
        c.segment = _assign_segment(c.r_score, c.f_score, c.m_score)

    return rfm_list


def generate_report(customers: List[CustomerRFM]) -> str:
    total = len(customers)
    total_revenue = sum(c.monetary for c in customers)

    segment_counts: Dict[str, List[CustomerRFM]] = defaultdict(list)
    for c in customers:
        segment_counts[c.segment].append(c)

    customers_sorted = sorted(customers, key=lambda c: c.monetary, reverse=True)
    top_20_count = max(1, int(total * 0.2))
    top_20_revenue = sum(c.monetary for c in customers_sorted[:top_20_count])
    pareto_pct = top_20_revenue / total_revenue * 100 if total_revenue else 0

    one_time = sum(1 for c in customers if c.frequency == 1)
    repeat = total - one_time

    lines: List[str] = []
    lines.append("# Customer Segmentation Report\n")

    lines.append("## Snapshot\n")
    lines.append(f"- **Total customers**: {total:,}")
    lines.append(f"- **One-time buyers**: {one_time:,} ({one_time / total * 100:.0f}%)")
    lines.append(f"- **Repeat buyers**: {repeat:,} ({repeat / total * 100:.0f}%)")
    lines.append(f"- **Total revenue**: ${total_revenue:,.0f}")
    lines.append(f"- **Top 20% customers drive**: {pareto_pct:.0f}% of revenue")
    avg_freq = sum(c.frequency for c in customers) / total if total else 0
    avg_clv = total_revenue / total if total else 0
    lines.append(f"- **Avg order frequency**: {avg_freq:.1f} orders")
    lines.append(f"- **Avg CLV**: ${avg_clv:.0f}\n")

    lines.append("## Segments\n")
    lines.append("| Segment | Customers | % | Avg spend | Avg orders | Action |")
    lines.append("|---------|----------:|--:|----------:|-----------:|--------|")

    segment_order = ["Champions", "Loyal", "Potential Loyalists", "New",
                     "Needs Attention", "At-Risk", "Can't Lose Them", "Hibernating", "Others"]
    for seg in segment_order:
        members = segment_counts.get(seg, [])
        if not members:
            continue
        cnt = len(members)
        pct = cnt / total * 100
        avg_spend = sum(c.monetary for c in members) / cnt
        avg_orders = sum(c.frequency for c in members) / cnt
        actions = {
            "Champions": "VIP perks, referral program",
            "Loyal": "Cross-sell, loyalty rewards",
            "Potential Loyalists": "Nurture, second-purchase offer",
            "New": "Welcome series, product education",
            "Needs Attention": "Re-engagement, personalized recs",
            "At-Risk": "Win-back flow, incentive",
            "Can't Lose Them": "Personal outreach, premium offer",
            "Hibernating": "Sunset flow or suppress",
            "Others": "Review and reclassify",
        }
        lines.append(
            f"| {seg} | {cnt:,} | {pct:.0f}% | ${avg_spend:.0f} "
            f"| {avg_orders:.1f} | {actions.get(seg, '')} |"
        )
    lines.append("")

    lines.append("## Top customers (VIPs)\n")
    lines.append("| Customer | Total spend | Orders | Last purchase (days ago) | Segment |")
    lines.append("|----------|------------:|-------:|------------------------:|---------|")
    for c in customers_sorted[:min(10, total)]:
        lines.append(
            f"| {c.email} | ${c.monetary:,.0f} | {c.frequency} "
            f"| {c.recency_days} | {c.segment} |"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="RFM segmentation from an order export CSV.")
    parser.add_argument("--in", dest="in_path", required=True, help="Path to order export CSV.")
    parser.add_argument("--out", dest="out_path", default=None, help="Output file (default: stdout).")
    parser.add_argument("--ref-date", default=None, help="Reference date YYYY-MM-DD (default: today).")
    args = parser.parse_args()

    in_path = Path(args.in_path).expanduser()
    if not in_path.exists():
        print(f"File not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    ref = datetime.strptime(args.ref_date, "%Y-%m-%d").date() if args.ref_date else date.today()
    customers = parse_orders(in_path, ref)
    report = generate_report(customers)

    if args.out_path:
        out_path = Path(args.out_path).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written to {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
