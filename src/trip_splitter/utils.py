# src/trip_splitter/utils.py
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple, Any


def compute_aggregates(
    expenses: Iterable[Dict[str, Any]],
    participants: Iterable[str],
):
    """
    Returns:
      - total (float)
      - person_spent: dict[name -> amount]
      - person_owes: dict[name -> amount]
      - category_spent: dict[category -> amount]
    """
    participants = list(participants)
    person_spent = defaultdict(float)
    person_owes = defaultdict(float)
    category_spent = defaultdict(float)

    total = 0.0

    for e in expenses:
        amount = float(e["amount"])
        total += amount
        paid_by = e["paid_by"]
        category = e.get("category", "Uncategorized")
        included = e.get("included", participants)

        # who paid
        person_spent[paid_by] += amount

        # category
        category_spent[category] += amount

        # fair share
        if included:
            share = amount / len(included)
            for p in included:
                person_owes[p] += share

    return total, dict(person_spent), dict(person_owes), dict(category_spent)


def compute_balances(
    expenses: Iterable[Dict[str, Any]],
    participants: Iterable[str],
):
    """
    Returns:
      - total
      - balances: dict[name -> balance]
      - person_spent
      - person_owes
      - category_spent
    """
    participants = list(participants)
    total, person_spent, person_owes, category_spent = compute_aggregates(
        expenses, participants
    )

    balances = {}
    for p in participants:
        spent = person_spent.get(p, 0.0)
        owes = person_owes.get(p, 0.0)
        balances[p] = round(spent - owes, 2)

    return total, balances, person_spent, person_owes, category_spent


def optimize_settlements(balances: Dict[str, float]) -> List[Tuple[str, str, float]]:
    """
    Same greedy algorithm you had:
    Takes balances dict (positive -> should receive, negative -> owes)
    Returns list of (debtor, creditor, amount)
    """
    creditors = {k: v for k, v in balances.items() if v > 0}
    debtors = {k: -v for k, v in balances.items() if v < 0}
    txns: List[Tuple[str, str, float]] = []

    # sort by amount descending
    creditors = dict(sorted(creditors.items(), key=lambda x: -x[1]))
    debtors = dict(sorted(debtors.items(), key=lambda x: -x[1]))

    for d in debtors:
        for c in creditors:
            if debtors[d] <= 0:
                break
            if creditors[c] <= 0:
                continue
            amt = round(min(debtors[d], creditors[c]), 2)
            if amt > 0:
                txns.append((d, c, amt))
                debtors[d] -= amt
                creditors[c] -= amt

    return txns
