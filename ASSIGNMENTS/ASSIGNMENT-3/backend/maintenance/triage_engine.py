"""
Deterministic and Explainable Triage Engine for Maintenance Tickets.
Applies university approved Impact x Urgency rule matrix and keyword taxonomy.
"""

from datetime import timedelta
from django.utils import timezone
from config.policies import SLA_RESOLUTION_MINUTES

PRIORITY_MATRIX = {
    ('high', 'high'): 'M1',
    ('high', 'medium'): 'M2',
    ('high', 'low'): 'M3',
    ('medium', 'high'): 'M2',
    ('medium', 'medium'): 'M3',
    ('medium', 'low'): 'M4',
    ('low', 'high'): 'M3',
    ('low', 'medium'): 'M4',
    ('low', 'low'): 'M4',
}

CATEGORY_KEYWORDS = {
    'hvac': ['ac', 'air-conditioning', 'chiller', 'temperature', 'overheat', 'fan', 'cooling', 'hvac', 'ventilation', 'thermostat'],
    'plumbing': ['leak', 'pipe', 'water', 'flood', 'drain', 'faucet', 'toilet', 'overflow', 'plumbing', 'sewage'],
    'electrical': ['spark', 'power', 'electrical', 'breaker', 'blackout', 'wiring', 'fuse', 'outlet', 'short-circuit', 'voltage'],
    'network': ['wifi', 'network', 'ethernet', 'router', 'switch', 'internet', 'connectivity', 'latency', 'gateway'],
    'structural': ['door', 'window', 'lock', 'ceiling', 'wall', 'crack', 'glass', 'hinge', 'roof'],
}

def classify_text(text: str):
    """Deterministically identifies maintenance category based on approved keyword vocabulary."""
    lower_text = text.lower()
    matched_rules = []
    best_category = 'general'

    for category, keywords in CATEGORY_KEYWORDS.items():
        found = [kw for kw in keywords if kw in lower_text]
        if found:
            matched_rules.append((category, found))

    if matched_rules:
        # Pick category with most keyword matches
        matched_rules.sort(key=lambda x: len(x[1]), reverse=True)
        best_category = matched_rules[0][0]
        explanation = f"Matched keyword(s) {matched_rules[0][1]} mapping to category '{best_category}'."
    else:
        best_category = 'general'
        explanation = "No domain keyword matched; assigned default 'general' category."

    return best_category, explanation

def calculate_priority(impact: str, urgency: str):
    """Calculates M1-M4 priority using the 3x3 Impact x Urgency matrix."""
    imp = impact.lower()
    urg = urgency.lower()
    priority = PRIORITY_MATRIX.get((imp, urg), 'M3')
    return priority

def triage_ticket(title: str, description: str, impact: str = 'medium', urgency: str = 'medium', override_category: str = None):
    """
    Executes end-to-end explainable triage.
    Returns: category, priority, sla_due_at, explanation
    """
    text = f"{title} {description}"
    detected_category, cat_explanation = classify_text(text)

    category = override_category if override_category and override_category != 'general' else detected_category
    priority = calculate_priority(impact, urgency)

    resolution_mins = SLA_RESOLUTION_MINUTES.get(priority, 480)
    sla_due_at = timezone.now() + timedelta(minutes=resolution_mins)

    explanation = (
        f"[Explainable Triage Engine]\n"
        f"1. Categorization: {cat_explanation}\n"
        f"2. Priority Assessment: Impact='{impact.upper()}' and Urgency='{urgency.upper()}' "
        f"evaluate via matrix to Priority {priority}.\n"
        f"3. SLA Target: Assigned resolution deadline of {resolution_mins} minutes ({resolution_mins/60:.1f} hours)."
    )

    return category, priority, sla_due_at, explanation
