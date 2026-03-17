import torch
import torch.nn as nn
import torch.nn.functional as F
from defenses.smoothing import apply_smoothing


# ── MRR: Modular Robust Redundancy ───────────────────────────────────────
# Based on "Safe Machine Learning and Defeating Adversarial Attacks" (UCSD)
#
# Core idea: instead of relying on a single model prediction, run the input
# through multiple independent "modules" (the same model with different
# input preprocessors) and aggregate their votes. An adversarial example
# crafted to fool one module is unlikely to fool all of them simultaneously.
#
# The three modules we use:
#   Module 1 — raw input (no preprocessing)
#   Module 2 — gaussian smoothed input
#   Module 3 — median smoothed input
#
# Final prediction = majority vote across all three modules.
# If all three disagree (no majority) we fall back to the most confident.


NUM_MODULES = 3


def run_mrr_defense(model, image_tensor, original_pred):
    """
    Runs the MRR defense on a given input tensor.

    Arguments:
        model          -- loaded PyTorch model in eval mode
        image_tensor   -- input tensor shape (1, 3, H, W)
        original_pred  -- the model's prediction WITHOUT defense (int)

    Returns a dict:
        {
            "mrr_pred":         int,    final MRR prediction
            "module_preds":     list,   prediction from each module
            "module_confs":     list,   confidence from each module
            "vote_counts":      dict,   {class: votes}
            "consensus":        bool,   True if majority agree
            "defense_changed":  bool,   True if MRR pred != original pred
            "description":      str
        }
    """
    model.eval()

    # ── Build the three input variants ───────────────────────────────────
    inputs = [
        image_tensor,                                              # raw
        apply_smoothing(image_tensor, method="gaussian", strength="medium"),
        apply_smoothing(image_tensor, method="median",   strength="medium"),
    ]

    module_preds = []
    module_confs = []

    with torch.no_grad():
        for inp in inputs:
            out   = model(inp)
            probs = torch.softmax(out, dim=1)
            pred  = int(probs.argmax(dim=1).item())
            conf  = float(probs.max().item()) * 100
            module_preds.append(pred)
            module_confs.append(round(conf, 2))

    # ── Majority vote ─────────────────────────────────────────────────────
    vote_counts = {}
    for pred in module_preds:
        vote_counts[pred] = vote_counts.get(pred, 0) + 1

    majority_class = max(vote_counts, key=vote_counts.get)
    majority_votes = vote_counts[majority_class]
    consensus      = majority_votes >= 2   # at least 2 of 3 agree

    if consensus:
        mrr_pred = majority_class
    else:
        # No majority — pick the module with highest confidence
        best_module = int(torch.tensor(module_confs).argmax().item())
        mrr_pred    = module_preds[best_module]

    defense_changed = (mrr_pred != original_pred)

    # ── Human readable description ────────────────────────────────────────
    module_names = ["Raw input", "Gaussian smoothed", "Median smoothed"]
    votes_str    = ", ".join(
        f"{module_names[i]} → class {module_preds[i]} ({module_confs[i]:.1f}%)"
        for i in range(NUM_MODULES)
    )

    if consensus:
        desc = (f"Majority consensus: {majority_votes}/{NUM_MODULES} modules "
                f"predicted class {mrr_pred}. {votes_str}")
    else:
        desc = (f"No majority — fell back to highest confidence module. "
                f"{votes_str}")

    return {
        "mrr_pred":        mrr_pred,
        "module_preds":    module_preds,
        "module_confs":    module_confs,
        "vote_counts":     vote_counts,
        "consensus":       consensus,
        "defense_changed": defense_changed,
        "description":     desc
    }


def evaluate_mrr_against_attacks(model, image_tensor, attack_results):
    """
    Runs MRR defense against each attack result and reports
    whether MRR would have prevented the misclassification.

    Arguments:
        model          -- loaded PyTorch model
        image_tensor   -- original clean input tensor
        attack_results -- dict returned by run_adversarial_tests()

    Returns a dict:
        {
            "fgsm_defended":     bool,
            "bim_defended":      bool,
            "deepfool_defended": bool,
            "total_defended":    int,
            "mrr_robustness_bonus": int,   extra points to add to score
            "details":           dict
        }
    """
    attack_keys  = ["fgsm", "bim", "deepfool"]
    details      = {}
    total_defended = 0

    for key in attack_keys:
        attack = attack_results.get(key, {})

        # Only evaluate if the attack succeeded (model was fooled)
        if not attack.get("success", False) or "error" in attack:
            details[key] = {
                "evaluated": False,
                "reason": "Attack did not succeed or errored — MRR not needed"
            }
            continue

        adv_image    = attack.get("adversarial_image")
        original_pred = attack.get("original_pred", 0)

        if adv_image is None:
            details[key] = {
                "evaluated": False,
                "reason": "No adversarial image returned by attack"
            }
            continue

        mrr_result = run_mrr_defense(
            model=model,
            image_tensor=adv_image,
            original_pred=original_pred
        )

        # MRR defends if it restores the original prediction
        defended = (mrr_result["mrr_pred"] == original_pred)
        if defended:
            total_defended += 1

        details[key] = {
            "evaluated":      True,
            "defended":       defended,
            "mrr_pred":       mrr_result["mrr_pred"],
            "original_pred":  original_pred,
            "consensus":      mrr_result["consensus"],
            "module_preds":   mrr_result["module_preds"],
            "module_confs":   mrr_result["module_confs"],
            "description":    mrr_result["description"]
        }

    # Bonus points: each attack defended by MRR adds to the robustness score
    # Weighted same as adversarial scoring
    bonus_weights = {"fgsm": 10, "bim": 15, "deepfool": 20}
    mrr_bonus = sum(
        bonus_weights[k]
        for k in attack_keys
        if details.get(k, {}).get("defended", False)
    )

    return {
        "fgsm_defended":        details.get("fgsm",     {}).get("defended", False),
        "bim_defended":         details.get("bim",      {}).get("defended", False),
        "deepfool_defended":    details.get("deepfool", {}).get("defended", False),
        "total_defended":       total_defended,
        "mrr_robustness_bonus": mrr_bonus,
        "details":              details
    }