#!/usr/bin/env python3
"""
Tag customers by lifecycle stage based on recency thresholds.

Reads an order export CSV, calculates days since last purchase per customer,
and assigns lifecycle stages: New, Active, At-Risk, Lapsed, Churned.

Usage:
    python3 scripts/lifecycle_tagger.py --in orders.csv --out lifecycle_report.md
    python3 scripts/lifecycle_tagger.py --in orders.csv --active 90 --lapsed 365
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List


@dataclass
class CustomerLifecycle:
    email: str
    first_order: date
    last_order: date
    order_count: int
    total_spend: float
    days_since_last: int
    stage: str = ""


def parse_orders(path: Path, ref_date: date) -> List[CustomerLifecycle]:
    customers: Dict[str, Dict] = defaultdict(lambda: {"dates": [], "amounts": []})

    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            email = row["customer_email"].strip().lower()
            order_date = datetime.strptime(row["order_date"].strip(), "%Y-%m-%d").date()
            amount = float(row["amount"])
            customers[email]["dates"].append(order_date)
            customers[email]["amounts"].append(amount)

    result: List[CustomerLifecycle] = []
    for email, data in customers.items():
        dates = data["dates"]
        result.append(CustomerLifecycle(
            email=email,
            first_order=min(dates),
            last_order=max(dates),
            order_count=len(dates),
            total_spend=sum(data["amounts"]),
            days_since_last=(ref_date - max(dates)).days,
        ))
    return result


def assign_stages(
    customers: List[CustomerLifecycle],
    new_days: int,
    active_days: int,
    at_risk_days: int,
    lapsed_days: int,
) -> None:
    for c in customers:
        if c.order_count == 1 and c.days_since_last <= new_days:
            c.stage = "New"
        elif c.days_since_last <= active_days:
            c.stage = "Active"
        elif c.days_since_last <= at_risk_days:
            c.stage = "At-Risk"
        elif c.days_since_last <= lapsed_days:
            c.stage = "Lapsed"
        else:
            c.stage = "Churned"


def generate_report(
    customers: List[CustomerLifecycle],
    active_days: int,
    at_risk_days: int,
    lapsed_days: int,
) -> str:
    total = len(customers)
    total_revenue = sum(c.total_spend for c in customers)

    stage_groups: Dict[str, List[CustomerLifecycle]] = defaultdict(list)
    for c in customers:
        stage_groups[c.stage].append(c)

    lines: List[str] = []
    lines.append("# Customer Lifecycle Report\n")

    lines.append("## Thresholds used\n")
    lines.append(f"- **Active**: last purchase ≤ {active_days} days ago")
    lines.append(f"- **At-Risk**: {active_days}–{at_risk_days} days")
    lines.append(f"- **Lapsed**: {at_risk_days}–{lapsed_days} days")
    lines.append(f"- **Churned**: > {lapsed_days} days\n")

    lines.append("## Lifecycle summary\n")
    lines.append("| Stage | Customers | % | Avg spend | Avg orders | Avg days since last |")
    lines.append("|-------|----------:|--:|----------:|-----------:|--------------------:|")

    for stage in ["New", "Active", "At-Risk", "Lapsed", "Churned"]:
        members = stage_groups.get(stage, [])
        if not members:
            continue
        cnt = len(members)
        pct = cnt / total * 100
        avg_spend = sum(c.total_spend for c in members) / cnt
        avg_orders = sum(c.order_count for c in members) / cnt
        avg_recency = sum(c.days_since_last for c in members) / cnt
        lines.append(
            f"| {stage} | {cnt:,} | {pct:.0f}% | ${avg_spend:.0f} "
            f"| {avg_orders:.1f} | {avg_recency:.0f} |"
        )
    lines.append("")

    lines.append("## Customer detail\n")
    lines.append("| Customer | Stage | Orders | Total spend | Last purchase | Days ago |")
    lines.append("|----------|-------|-------:|------------:|--------------:|---------:|")
    for c in sorted(customers, key=lambda x: x.days_since_last):
        lines.append(
            f"| {c.email} | {c.stage} | {c.order_count} | ${c.total_spend:,.0f} "
            f"| {c.last_order} | {c.days_since_last} |"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tag customers by lifecycle stage from order data.")
    parser.add_argument("--in", dest="in_path", required=True, help="Path to order export CSV.")
    parser.add_argument("--out", dest="out_path", default=None, help="Output file (default: stdout).")
    parser.add_argument("--new", type=int, default=30, help="Days for 'New' stage (single-purchase, recent).")
    parser.add_argument("--active", type=int, default=90, help="Days threshold for 'Active'.")
    parser.add_argument("--at-risk", type=int, default=180, help="Days threshold for 'At-Risk'.")
    parser.add_argument("--lapsed", type=int, default=365, help="Days threshold for 'Lapsed' (beyond = Churned).")
    parser.add_argument("--ref-date", default=None, help="Reference date YYYY-MM-DD (default: today).")
    args = parser.parse_args()

    in_path = Path(args.in_path).expanduser()
    if not in_path.exists():
        print(f"File not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    ref = datetime.strptime(args.ref_date, "%Y-%m-%d").date() if args.ref_date else date.today()
    customers = parse_orders(in_path, ref)
    assign_stages(customers, args.new, args.active, args.at_risk, args.lapsed)
    report = generate_report(customers, args.active, args.at_risk, args.lapsed)

    if args.out_path:
        out_path = Path(args.out_path).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written to {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
