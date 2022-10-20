what_if_explanations = [
    "event_stats_AND_what_if",
    "event_stats_OR_what_if",
    "why_how_to_explanation",
    "interaction_addition_hover_what_if",
    "interaction_or_hover_what_if",
    "queried_axiom_why/why_not",
]

how_to_explanations = ["why_how_to_explanation"]


def get_explanations(data):
    explanations = []
    for d in data:
        data_msg = d["msg"]
        if data_msg in what_if_explanations:
            explanations.append(d)
        elif data_msg == "what_if":
            if (
                "interaction_addition_hover_what_if" in d
                or "interaction_or_hover_what_if" in d
            ):
                explanations.append(d)

    return explanations


def get_prev_explanations(axioms, idx, explanations):

    ax_explanations = []
    axiom = axioms[idx]
    prev_axiom = axioms[idx - 1]

    t1 = prev_axiom["timestamp"] if idx > 0 else 0
    t2 = axiom["timestamp"]
    for ex in explanations:
        t_ex = ex["timestamp"]
        if t1 < t_ex < t2:
            ax_explanations.append(ex)

    return ax_explanations
