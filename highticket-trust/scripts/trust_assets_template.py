"""
Helper for the `high-ticket-trust-conversion` skill.

Provides a structured template for high-ticket trust assets so that different
agents or runs can refer to the same categories and keys when generating
checklists or tables.

Typical usage:

    from trust_assets_template import TRUST_ASSET_CATEGORIES, as_markdown_table

    print(as_markdown_table())
"""

from __future__ import annotations

from typing import Dict, List


TRUST_ASSET_CATEGORIES: Dict[str, List[str]] = {
    "Brand & credentials": [
        "Brand history and story",
        "Certifications / test reports",
        "Store / factory / showroom",
        "Awards and press",
    ],
    "Expertise & offer": [
        "Core team and background",
        "Service / build / teaching process",
        "Methodology and standards",
        "Strong case studies and results",
    ],
    "Delivery & risk": [
        "Production / build / service steps and QC",
        "Delay / incident handling",
        "After-sales and warranty",
        "Fallback when customer is unhappy",
    ],
    "Price & value": [
        "Pricing logic and breakdown",
        "Vs cheaper alternatives",
        "Long-term cost / benefit",
        "Extra value-added services",
    ],
    "Social proof": [
        "Real reviews and follow-ups",
        "Client stories and interviews",
        "Video / image proof",
        "Repeat and referral data",
    ],
}


def as_markdown_table() -> str:
    """
    Render the trust asset categories as a markdown table skeleton that the
    skill can embed in its outputs and then fill with concrete items.
    """
    lines: List[str] = []
    lines.append("| Category | Element | Have today? | Add in 30 days | Notes |")
    lines.append("| --- | --- | --- | --- | --- |")

    for category, items in TRUST_ASSET_CATEGORIES.items():
        for item in items:
            lines.append(f"| {category} | {item} |  |  |  |")

    return "\n".join(lines)


if __name__ == "__main__":
    print(as_markdown_table())
