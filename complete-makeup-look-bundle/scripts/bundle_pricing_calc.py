#!/usr/bin/env python3
"""
Bundle pricing calculator for "Complete the Look" bundles.

Calculates bundle price, savings vs buying separately, and margin impact
at different discount levels.

Usage:
    python3 bundle_pricing_calc.py --items "Foundation:35,Sponge:12,Setting Spray:18" --discount-pct 10
    python3 bundle_pricing_calc.py --items "Lip Liner:14,Lipstick:22,Lip Gloss:16" --discount-pct 15 --margin-floor 50
"""

import argparse
import sys


def parse_items(items_str: str) -> list[tuple[str, float]]:
    items = []
    for part in items_str.split(","):
        part = part.strip()
        if ":" not in part:
            raise ValueError(f"Invalid item format: '{part}'. Use 'Name:Price'.")
        name, price_str = part.rsplit(":", 1)
        items.append((name.strip(), float(price_str.strip())))
    return items


def calculate_bundle(
    items: list[tuple[str, float]],
    discount_pct: float,
    cogs_pct: float = 40.0,
    margin_floor: float = 0.0,
) -> dict:
    total_retail = sum(price for _, price in items)
    discount_amount = total_retail * (discount_pct / 100.0)
    bundle_price = total_retail - discount_amount

    cogs = total_retail * (cogs_pct / 100.0)
    single_margin_pct = (1 - cogs_pct / 100.0) * 100
    bundle_margin = bundle_price - cogs
    bundle_margin_pct = (bundle_margin / bundle_price * 100) if bundle_price > 0 else 0
    margin_ok = bundle_margin_pct >= margin_floor

    return {
        "items": items,
        "item_count": len(items),
        "total_retail": round(total_retail, 2),
        "discount_pct": discount_pct,
        "discount_amount": round(discount_amount, 2),
        "bundle_price": round(bundle_price, 2),
        "cogs_pct": cogs_pct,
        "cogs": round(cogs, 2),
        "single_margin_pct": round(single_margin_pct, 1),
        "bundle_margin": round(bundle_margin, 2),
        "bundle_margin_pct": round(bundle_margin_pct, 1),
        "margin_floor": margin_floor,
        "margin_ok": margin_ok,
    }


def format_report(r: dict) -> str:
    lines = [
        "",
        "=" * 55,
        "  COMPLETE THE LOOK — BUNDLE PRICING",
        "=" * 55,
        "",
        "  ITEMS IN BUNDLE:",
    ]
    for name, price in r["items"]:
        lines.append(f"    {name:<25} ${price:>8.2f}")
    lines.extend([
        "",
        "-" * 55,
        f"  Total if bought separately:   ${r['total_retail']:>8.2f}",
        f"  Bundle discount:              {r['discount_pct']:>7.1f}%",
        f"  Discount amount:              ${r['discount_amount']:>8.2f}",
        f"  BUNDLE PRICE:                 ${r['bundle_price']:>8.2f}",
        "",
        "-" * 55,
        "  MARGIN ANALYSIS",
        "-" * 55,
        f"  Est. COGS ({r['cogs_pct']:.0f}% of retail):  ${r['cogs']:>8.2f}",
        f"  Single-item margin:           {r['single_margin_pct']:>7.1f}%",
        f"  Bundle margin:                {r['bundle_margin_pct']:>7.1f}%",
        f"  Bundle margin ($):            ${r['bundle_margin']:>8.2f}",
    ])

    if r["margin_floor"] > 0:
        status = "PASS" if r["margin_ok"] else "FAIL"
        lines.append(f"  Margin floor ({r['margin_floor']:.0f}%):          {status}")
        if not r["margin_ok"]:
            lines.append(f"  ⚠  Bundle margin is below your {r['margin_floor']:.0f}% floor.")
            lines.append(f"     Consider reducing discount or removing lower-margin items.")

    lines.extend([
        "",
        "-" * 55,
        "  COPY SUGGESTION",
        "-" * 55,
    ])

    if r["discount_pct"] > 0:
        lines.append(f'  "Save ${r["discount_amount"]:.0f} when you complete the look"')
        lines.append(f'  "Bundle & save {r["discount_pct"]:.0f}% — get all {r["item_count"]} in one click"')
    else:
        lines.append(f'  "One click, one complete look — ${r["bundle_price"]:.0f}"')
        lines.append(f'  "Get everything you need in one step"')

    lines.extend(["", "=" * 55])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate bundle price, savings, and margin impact"
    )
    parser.add_argument(
        "--items", required=True,
        help='Items as "Name:Price,Name:Price,..." (e.g. "Foundation:35,Sponge:12")',
    )
    parser.add_argument(
        "--discount-pct", type=float, default=0,
        help="Bundle discount percentage (default: 0 = no discount)",
    )
    parser.add_argument(
        "--cogs-pct", type=float, default=40,
        help="Estimated COGS as %% of retail (default: 40)",
    )
    parser.add_argument(
        "--margin-floor", type=float, default=0,
        help="Minimum acceptable margin %% (default: 0 = no floor check)",
    )
    args = parser.parse_args()

    try:
        items = parse_items(args.items)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    result = calculate_bundle(items, args.discount_pct, args.cogs_pct, args.margin_floor)
    print(format_report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
