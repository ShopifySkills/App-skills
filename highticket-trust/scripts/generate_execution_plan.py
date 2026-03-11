"""
Utility script for the `high-ticket-trust-conversion` skill.

Given a list of focus areas, this script generates a simple 2–4 week execution
plan with weekly themes and tasks. It is intentionally lightweight and designed
for manual tweaking by the user.

Usage (example):

    from generate_execution_plan import generate_plan, print_plan

    focus_areas = [
        "Fill trust assets (cases, credentials, client stories)",
        "Optimize landing/PDP hero and trust modules",
        "Clarify sales/CS first-touch and quote talking points",
        "Set up 14–30 day lead nurture rhythm"
    ]

    plan = generate_plan(focus_areas, weeks=4)
    print_plan(plan)
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class WeeklyTask:
    week: int
    theme: str
    tasks: List[str]


def generate_plan(focus_areas: List[str], weeks: int = 4) -> List[WeeklyTask]:
    """
    Generate a simple weekly execution plan from high-level focus areas.

    - Distributes focus areas roughly across the given number of weeks.
    - For each focus area, creates 2–3 concrete tasks as suggestions.
    """
    if weeks <= 0:
        raise ValueError("weeks must be positive")

    def expand_focus_to_tasks(area: str) -> List[str]:
        return [
            f"Audit/organize: {area}",
            f"Draft first version of plan or copy: {area}",
            f"Internal review and one iteration: {area}",
        ]

    weekly_plan: List[WeeklyTask] = []
    for i in range(weeks):
        if focus_areas:
            area_index = min(i, len(focus_areas) - 1)
            theme = focus_areas[area_index]
            tasks = expand_focus_to_tasks(theme)
        else:
            theme = "Customize focus for this week"
            tasks = ["Set 1 main trust/conversion goal", "Break into 3–5 actions and schedule"]

        weekly_plan.append(
            WeeklyTask(
                week=i + 1,
                theme=theme,
                tasks=tasks,
            )
        )

    return weekly_plan


def plan_to_dict(plan: List[WeeklyTask]) -> List[Dict[str, Any]]:
    """Convert a plan to a list of serializable dicts."""
    return [asdict(item) for item in plan]


def print_plan(plan: List[WeeklyTask]) -> None:
    """Pretty-print the plan in a CLI-friendly format."""
    for item in plan:
        print(f"Week {item.week}: {item.theme}")
        for idx, task in enumerate(item.tasks, start=1):
            print(f"  {idx}. {task}")
        print()


if __name__ == "__main__":
    default_focus = [
        "Fill trust assets (cases, credentials, client stories)",
        "Optimize key page hero and trust modules",
        "Optimize inquiry/sales copy and SOP",
        "Set up 14–30 day lead nurture rhythm",
    ]
    plan = generate_plan(default_focus, weeks=4)
    print_plan(plan)
