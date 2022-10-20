import json


def get_formulas(data_list):
    formulas = []
    for d in data_list:
        if d["msg"] == "formula_save":
            formula = d["formula"]
            formula["timestamp"] = d["timestamp"]
            formulas.append(formula)

    return formulas


def get_axioms(data_list):
    axioms = []
    for i, d in enumerate(data_list):
        new_axiom = None
        if d["msg"] == "new_axiom":
            activity = d["activity"]
            for j in range(i):
                if data_list[i - j]["msg"] == "activities":
                    for act in data_list[i - j]["activities"]:
                        if act["name"] == activity["name"]:
                            new_axiom = _get_new_axiom(act, activity)
                            res1 = _find_prev("classification_result", data_list, i)[
                                "classification"
                            ]
                            res2 = _find_next("classification_result", data_list, i)[
                                "classification"
                            ]
                            ax_changes = _get_changes(res1, res2)
                            new_axiom["improved"] = (
                                True if ax_changes["is_improved"] else False
                            )
                            new_axiom["timestamp"] = d["timestamp"]
                            new_axiom["tp_inc"] = ax_changes["tp_inc"]
                            new_axiom["fp_dec"] = ax_changes["fp_dec"]
                            break
                    else:
                        continue
                    break

            axioms.append(new_axiom)

    return axioms


def _get_new_axiom(act1, act2):
    if json.dumps(sorted(act1["constraints"])) != json.dumps(
        sorted(act2["constraints"])
    ):
        return {
            "axiom": act2["constraints"][-1],
            "type": act2["constraints"][-1]["type"],
        }

    if json.dumps(sorted(act1["eventORList"])) != json.dumps(
        sorted(act2["eventORList"])
    ):
        return {"axiom": act2["eventORList"], "type": "interaction_or"}

    if json.dumps(sorted(act1["excludedEvents"])) != json.dumps(
        sorted(act2["excludedEvents"])
    ):
        return {"axiom": sorted(act2["excludedEvents"]), "type": "interaction_negation"}

    return {"axiom": sorted(act2["events"]), "type": "interaction"}


def _find_next(msg, data, idx):
    for i in range(idx + 1, len(data)):
        if data[i]["msg"] == msg:
            return data[i]
    return None


def _find_prev(msg, data, idx):
    for i in range(idx - 1, -1, -1):
        if data[i]["msg"] == msg:
            return data[i]
    return None


def _get_changes(res1, res2):
    # pre-condition: only one activity in result
    r1 = res1[list(res1.keys())[0]]
    r2 = res2[list(res2.keys())[0]]

    tp_inc = len(r2["TP"]) - len(r1["TP"])
    fp_dec = len(r1["FP"]["all"]) - len(r2["FP"]["all"])

    return {"is_improved": tp_inc > 0 or fp_dec > 0, "tp_inc": tp_inc, "fp_dec": fp_dec}


def get_data(data, t1, t2):
    return list(filter(lambda d: t1 < d["timestamp"] < t2, data))
