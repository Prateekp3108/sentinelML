import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


# ── Anomaly Index threshold from Neural Cleanse paper ────────────────────
# If a class has an anomaly index > 2.0 it is flagged as a trojan target
ANOMALY_THRESHOLD = 2.0

# How many classes to scan (cap for speed — full scan on 1000 classes is too slow)
MAX_CLASSES_TO_SCAN = 10

# Optimisation steps per class
OPTIMISATION_STEPS = 100


def run_trojan_detection(model, input_size, num_classes, status_callback=None):
    """
    Runs Neural Cleanse-based trojan detection on a model.

    For each candidate target class we find the smallest trigger mask+pattern
    that causes any input to be classified as that class. If one class needs
    a much smaller trigger than the others, it is likely a backdoor target.

    Returns a dict:
        {
            "trojan_detected": bool,
            "confidence": str,          # "High" / "Medium" / "Low"
            "anomaly_index": float,
            "suspected_target_class": int or None,
            "trigger_norms": list,
            "classes_scanned": int,
            "error": str or None        # only present on failure
        }
    """

    def update(msg):
        if status_callback:
            status_callback(msg)

    try:
        model.eval()
        classes_to_scan = min(num_classes, MAX_CLASSES_TO_SCAN)
        trigger_norms = []

        update(f"Scanning {classes_to_scan} classes for backdoor triggers...")

        for target_class in range(classes_to_scan):
            update(f"Analysing class {target_class + 1} of {classes_to_scan}...")

            norm = _find_trigger_norm(
                model=model,
                input_size=input_size,
                target_class=target_class,
                steps=OPTIMISATION_STEPS
            )
            trigger_norms.append(norm)

        update("Computing anomaly index...")

        anomaly_index, suspected_class = _compute_anomaly_index(trigger_norms)

        trojan_detected = anomaly_index > ANOMALY_THRESHOLD

        if anomaly_index > 3.0:
            confidence = "High"
        elif anomaly_index > 2.0:
            confidence = "Medium"
        else:
            confidence = "Low"

        update("Trojan scan complete")

        return {
            "trojan_detected": trojan_detected,
            "confidence": confidence if trojan_detected else "N/A",
            "anomaly_index": round(float(anomaly_index), 3),
            "suspected_target_class": int(suspected_class) if trojan_detected else None,
            "trigger_norms": [round(float(n), 4) for n in trigger_norms],
            "classes_scanned": classes_to_scan,
            "error": None
        }

    except Exception as e:
        return {
            "trojan_detected": False,
            "confidence": "N/A",
            "anomaly_index": 0.0,
            "suspected_target_class": None,
            "trigger_norms": [],
            "classes_scanned": 0,
            "error": str(e)
        }


def _find_trigger_norm(model, input_size, target_class, steps=100):
    """
    For a given target class, optimise a trigger mask + pattern that
    causes a random input to be classified as target_class.
    Returns the L1 norm of the optimised mask (smaller = easier to trigger = suspicious).
    """

    # Random base image
    image = torch.rand(1, 3, input_size, input_size, requires_grad=False)

    # Mask and pattern — both learnable
    # mask  : [0,1] per pixel — how much of the trigger to apply
    # pattern: [0,1] per pixel — the trigger pattern itself
    mask_raw    = torch.zeros(1, 1, input_size, input_size, requires_grad=True)
    pattern_raw = torch.rand(1, 3, input_size, input_size, requires_grad=True)

    optimizer = optim.Adam([mask_raw, pattern_raw], lr=0.01)
    criterion = nn.CrossEntropyLoss()
    target    = torch.tensor([target_class])

    # Weight for mask size regularisation — encourages small triggers
    lambda_reg = 0.01

    for _ in range(steps):
        optimizer.zero_grad()

        mask    = torch.sigmoid(mask_raw)           # squash to [0,1]
        pattern = torch.sigmoid(pattern_raw)        # squash to [0,1]

        # Apply trigger: blend pattern into image using mask
        triggered = (1 - mask) * image + mask * pattern
        triggered = torch.clamp(triggered, 0, 1)

        output = model(triggered)
        loss   = criterion(output, target) + lambda_reg * torch.norm(mask, p=1)

        loss.backward()
        optimizer.step()

    # Return the L1 norm of the final mask
    with torch.no_grad():
        final_mask = torch.sigmoid(mask_raw)
        norm = torch.norm(final_mask, p=1).item()

    return norm


def _compute_anomaly_index(norms):
    """
    Computes the anomaly index using the MAD (Median Absolute Deviation) method
    from the Neural Cleanse paper.

    A class whose trigger norm is much smaller than the median has an
    anomaly index > 2.0 and is flagged as a potential backdoor target.

    Returns (anomaly_index, suspected_class_index).
    """
    norms_array = np.array(norms)

    if len(norms_array) < 2:
        return 0.0, 0

    median = np.median(norms_array)
    mad    = np.median(np.abs(norms_array - median))

    # Avoid division by zero
    if mad < 1e-6:
        mad = 1e-6

    # Anomaly index for each class
    anomaly_indices = np.abs(norms_array - median) / mad

    # The most suspicious class is the one with the smallest norm
    suspected_class = int(np.argmin(norms_array))
    anomaly_index   = float(anomaly_indices[suspected_class])

    return anomaly_index, suspected_class