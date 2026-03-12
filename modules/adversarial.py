import torch
from attacks.fgsm import fgsm_attack
from attacks.bim import bim_attack
from attacks.deepfool import deepfool_attack


def get_test_image(input_size):
    return torch.rand(1, 3, input_size, input_size)


def run_adversarial_tests(model, input_size, num_classes, status_callback=None):

    def update(msg):
        if status_callback:
            status_callback(msg)

    results = {}

    # ── Prepare image ─────────────────────────────────────────────────────
    update("Preparing test image...")
    image = get_test_image(input_size)

    with torch.no_grad():
        output = model(image)
        predicted_label = output.argmax(dim=1)

    # ── FGSM ──────────────────────────────────────────────────────────────
    update("Running FGSM attack...")
    try:
        results["fgsm"] = fgsm_attack(
            model=model,
            image_tensor=image,
            true_label=predicted_label,
            epsilon=0.1
        )
        update("FGSM complete")
    except Exception as e:
        results["fgsm"] = {"success": False, "error": str(e)}
        update("FGSM failed")

    # ── BIM ───────────────────────────────────────────────────────────────
    update("Running BIM attack...")
    try:
        results["bim"] = bim_attack(
            model=model,
            image_tensor=image,
            true_label=predicted_label,
            epsilon=0.1,
            alpha=0.01,
            iterations=10
        )
        update("BIM complete")
    except Exception as e:
        results["bim"] = {"success": False, "error": str(e)}
        update("BIM failed")

    # ── DeepFool ──────────────────────────────────────────────────────────
    update("Running DeepFool attack...")
    try:
        results["deepfool"] = deepfool_attack(
            model=model,
            image_tensor=image,
            num_classes=min(num_classes, 10),
            max_iterations=20
        )
        update("DeepFool complete")
    except Exception as e:
        results["deepfool"] = {"success": False, "error": str(e)}
        update("DeepFool failed")

    # ── Score ─────────────────────────────────────────────────────────────
    update("Scoring results...")

    attacks_resisted = sum([
        not results["fgsm"].get("success", True),
        not results["bim"].get("success", True),
        not results["deepfool"].get("success", True),
    ])

    weighted_score = 0
    if not results["fgsm"].get("success", True):
        weighted_score += 25
    if not results["bim"].get("success", True):
        weighted_score += 35
    if not results["deepfool"].get("success", True):
        weighted_score += 40

    results["robustness_score"] = weighted_score
    results["attacks_resisted"] = attacks_resisted

    return results