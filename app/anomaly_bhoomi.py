"""Helpers for identifying unusual project costs."""

from __future__ import annotations

from numbers import Real
from statistics import median
from typing import Any, Iterable, Mapping


def _percentile(values: list[float], percentile: float) -> float:
    """Return a linearly interpolated percentile for sorted values."""
    if not values:
        raise ValueError("values must not be empty")

    position = (len(values) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    fraction = position - lower
    return values[lower] + (values[upper] - values[lower]) * fraction


def detect_cost_outliers(
    costs: Iterable[Real], multiplier: float = 1.5
) -> list[float]:
    """Return project costs outside the IQR outlier fences.

    Args:
        costs: An iterable of numeric project costs.
        multiplier: IQR multiplier used for the lower and upper fences.

    Returns:
        The original cost values that fall outside the IQR fences, preserving
        their input order.

    Raises:
        ValueError: If the multiplier is negative or no costs are supplied.
        TypeError: If a cost is not a real number.
    """
    if multiplier < 0:
        raise ValueError("multiplier must be non-negative")

    values = list(costs)
    if not values:
        raise ValueError("costs must not be empty")
    if not all(isinstance(cost, Real) for cost in values):
        raise TypeError("costs must contain only real numbers")

    sorted_values = sorted(float(cost) for cost in values)
    first_quartile = _percentile(sorted_values, 0.25)
    third_quartile = _percentile(sorted_values, 0.75)
    interquartile_range = third_quartile - first_quartile
    lower_fence = first_quartile - multiplier * interquartile_range
    upper_fence = third_quartile + multiplier * interquartile_range

    return [
        float(cost)
        for cost in values
        if cost < lower_fence or cost > upper_fence
    ]


def detect_grouped_cost_outliers(
    projects: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Flag projects whose amount is more than three times their group median.

    Projects are grouped by the ``district`` and ``workcategory`` fields.
    Returned records are copies of flagged projects with ``group_median`` and
    ``threshold`` fields added for reporting.
    """
    records = [dict(project) for project in projects]
    if not records:
        return []

    grouped_amounts: dict[tuple[Any, Any], list[float]] = {}
    for record in records:
        for field in ("district", "workcategory", "amount"):
            if field not in record:
                raise KeyError(f"project is missing required field: {field}")
        if not isinstance(record["amount"], Real):
            raise TypeError("project amounts must be real numbers")

        group = (record["district"], record["workcategory"])
        grouped_amounts.setdefault(group, []).append(float(record["amount"]))

    group_medians = {
        group: float(median(amounts))
        for group, amounts in grouped_amounts.items()
    }

    flagged: list[dict[str, Any]] = []
    for record in records:
        group = (record["district"], record["workcategory"])
        group_median = group_medians[group]
        threshold = group_median * 3
        if record["amount"] > threshold:
            flagged.append(
                {
                    **record,
                    "group_median": group_median,
                    "threshold": threshold,
                }
            )

    return flagged


if __name__ == "__main__":
    sample_costs = [12000, 13500, 14200, 15000, 15800, 16400, 17200, 95000]
    print("Sample costs:", sample_costs)
    print("Detected outliers:", detect_cost_outliers(sample_costs))

    sample_projects = [
        {"id": 1, "district": "North", "workcategory": "Roads", "amount": 100},
        {"id": 2, "district": "North", "workcategory": "Roads", "amount": 120},
        {"id": 3, "district": "North", "workcategory": "Roads", "amount": 800},
        {"id": 4, "district": "North", "workcategory": "Water", "amount": 200},
        {"id": 5, "district": "North", "workcategory": "Water", "amount": 220},
        {"id": 6, "district": "South", "workcategory": "Roads", "amount": 900},
    ]
    print("Grouped outliers:", detect_grouped_cost_outliers(sample_projects))
