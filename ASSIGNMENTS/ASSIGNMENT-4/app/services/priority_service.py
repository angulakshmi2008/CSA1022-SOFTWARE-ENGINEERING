"""
Priority matrix evaluation and keyword-based maintenance ticket triage.
"""

import re
from typing import Dict, List

# 9-cell impact and urgency matrix
PRIORITY_MATRIX: Dict[str, Dict[str, str]] = {
    "High": {
        "High": "M1",
        "Medium": "M2",
        "Low": "M3",
    },
    "Medium": {
        "High": "M2",
        "Medium": "M3",
        "Low": "M4",
    },
    "Low": {
        "High": "M3",
        "Medium": "M4",
        "Low": "M4",
    },
}

ALLOWED_IMPACT_LEVELS = {"High", "Medium", "Low"}
ALLOWED_URGENCY_LEVELS = {"High", "Medium", "Low"}

# Keyword dictionary for category triage
CATEGORY_KEYWORDS = {
    "Facilities": [
        "water",
        "leak",
        "ceiling",
        "pipe",
        "plumbing",
        "roof",
        "door",
        "lock",
        "window",
        "furniture",
    ],
    "HVAC": [
        "temperature",
        "cooling",
        "heating",
        "ac",
        "hvac",
        "thermostat",
        "airflow",
        "chiller",
        "ventilation",
    ],
    "AV-Network": [
        "projector",
        "screen",
        "display",
        "wifi",
        "network",
        "ethernet",
        "audio",
        "microphone",
        "hdmi",
        "cable",
    ],
}


def calculate_priority(impact: str, urgency: str) -> str:
    """
    Calculate priority from impact and urgency using the 9-cell matrix.
    Raises ValueError on invalid impact or urgency.
    """
    if not isinstance(impact, str) or impact not in ALLOWED_IMPACT_LEVELS:
        raise ValueError(
            f"Invalid impact level: '{impact}'. Must be one of {sorted(ALLOWED_IMPACT_LEVELS)}"
        )

    if not isinstance(urgency, str) or urgency not in ALLOWED_URGENCY_LEVELS:
        raise ValueError(
            f"Invalid urgency level: '{urgency}'. Must be one of {sorted(ALLOWED_URGENCY_LEVELS)}"
        )

    return PRIORITY_MATRIX[impact][urgency]


def classify_category(text: str) -> str:
    """
    Classify maintenance category from description text.
    - Water leak -> Facilities
    - Equal evidence tie -> Manual Review
    - Unknown terminology (no matches) -> Manual Review
    """
    if not text or not text.strip():
        return "Manual Review"

    text_lower = text.lower()

    scores: Dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            # Use whole-word boundary matching so 'ac' does not match 'oscillates' or 'practice'
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, text_lower):
                score += 1
        scores[category] = score

    best_score = max(scores.values())

    # If no keywords matched, triage to Manual Review
    if best_score == 0:
        return "Manual Review"

    # Identify categories with the highest score
    winners: List[str] = [cat for cat, score in scores.items() if score == best_score]

    # If there is a tie, triage to Manual Review
    if len(winners) != 1:
        return "Manual Review"

    return winners[0]
