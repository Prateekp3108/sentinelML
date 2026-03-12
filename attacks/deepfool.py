import torch
import torch.nn as nn


def deepfool_attack(model, image_tensor, num_classes=10, max_iterations=50, overshoot=0.02):
    """
    DeepFool Attack.
    Finds the MINIMUM perturbation needed to cross the decision boundary.
    Much more precise than FGSM or BIM — produces smallest possible noise.

    Arguments:
        model          -- the victim PyTorch model
        image_tensor   -- input image tensor, shape (1, 3, H, W)
        num_classes    -- number of output classes the model has
        max_iterations -- maximum steps to take before giving up
        overshoot      -- small extra push to ensure we cross the boundary

    Returns same dict structure as fgsm and bim attacks
    """

    model.eval()

    # ── Step 1: Get original prediction ─────────────────────────────────
    with torch.no_grad():
        original_output = model(image_tensor)
        original_probs = torch.softmax(original_output, dim=1)
        original_pred = original_output.argmax(dim=1).item()
        original_conf = original_probs[0][original_pred].item()

    # If model is already wrong, no attack needed
    true_label = original_pred


    # ── Step 2: Setup ────────────────────────────────────────────────────
    # Work on a copy of the image
    # We'll keep updating this as we iterate
    perturbed_image = image_tensor.clone().detach()
    total_perturbation = torch.zeros_like(image_tensor)

    current_pred = original_pred
    iteration = 0


    # ── Step 3: Main loop ────────────────────────────────────────────────
    # Keep iterating until the prediction changes OR we hit max iterations
    while current_pred == true_label and iteration < max_iterations:

        perturbed_image.requires_grad_(True)
        output = model(perturbed_image)

        # ── Step 4: Compute gradients for all classes ────────────────────
        # This is what makes DeepFool different from FGSM
        # Instead of just following the loss gradient,
        # we look at gradients toward ALL other classes
        # and find the CLOSEST decision boundary

        # Gradient for the correct class
        model.zero_grad()
        output[0, true_label].backward(retain_graph=True)
        grad_true = perturbed_image.grad.data.clone()

        # Find the closest boundary among all other classes
        min_distance = float('inf')
        best_perturbation = None

        for k in range(output.shape[1]):
            if k == true_label:
                continue

            # Gradient for class k
            model.zero_grad()
            perturbed_image.grad = None
            perturbed_image.requires_grad_(True)
            output2 = model(perturbed_image)
            output2[0, k].backward(retain_graph=True)
            grad_k = perturbed_image.grad.data.clone()

            # ── Step 5: Calculate distance to boundary for class k ───────
            # The boundary between true_label and k is a hyperplane
            # We calculate how far we need to move to cross it
            # Formula: |f_k - f_true| / ||grad_k - grad_true||
            w_k = grad_k - grad_true
            f_k = (output2[0, k] - output2[0, true_label]).item()

            distance = abs(f_k) / (w_k.norm().item() + 1e-8)

            if distance < min_distance:
                min_distance = distance
                best_perturbation = w_k


        # ── Step 6: Move toward the closest boundary ─────────────────────
        # Scale the perturbation by the distance
        # Add overshoot to make sure we actually cross it
        if best_perturbation is not None:
            step = (min_distance + 1e-4) * best_perturbation
            step = step / (best_perturbation.norm() + 1e-8)
            step = step * (1 + overshoot)

            total_perturbation = total_perturbation + step
            perturbed_image = image_tensor + total_perturbation
            perturbed_image = torch.clamp(perturbed_image, 0, 1).detach()

        # ── Step 7: Check if prediction changed ──────────────────────────
        with torch.no_grad():
            current_output = model(perturbed_image)
            current_pred = current_output.argmax(dim=1).item()

        iteration += 1


    # ── Step 8: Get final results ─────────────────────────────────────────
    with torch.no_grad():
        final_output = model(perturbed_image)
        final_probs = torch.softmax(final_output, dim=1)
        final_pred = final_output.argmax(dim=1).item()
        final_conf = final_probs[0][final_pred].item()

    attack_succeeded = (final_pred != true_label)

    return {
        "success": attack_succeeded,
        "adversarial_image": perturbed_image,
        "original_pred": original_pred,
        "adversarial_pred": final_pred,
        "original_conf": round(original_conf * 100, 2),
        "adversarial_conf": round(final_conf * 100, 2),
        "perturbation": total_perturbation.detach(),
        "iterations_used": iteration,
        "epsilon": total_perturbation.norm().item(),
    }