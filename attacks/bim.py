import torch
import torch.nn as nn


def bim_attack(model, image_tensor, true_label, epsilon=0.1, alpha=0.01, iterations=10):
    """
    Basic Iterative Method (BIM) attack.
    Essentially FGSM applied multiple times with small steps.

    Arguments:
        model         -- the victim PyTorch model
        image_tensor  -- input image tensor, shape (1, 3, H, W)
        true_label    -- correct class index as tensor
        epsilon       -- maximum total perturbation budget
        alpha         -- step size per iteration (should be < epsilon)
        iterations    -- how many steps to take
    
    Returns same dict structure as fgsm_attack
    """

    model.eval()
    loss_fn = nn.CrossEntropyLoss()

    # ── Step 1: Get original prediction ─────────────────────────────────
    with torch.no_grad():
        original_output = model(image_tensor)
        original_probs = torch.softmax(original_output, dim=1)
        original_pred = original_output.argmax(dim=1).item()
        original_conf = original_probs[0][original_pred].item()


    # ── Step 2: Start from the original image ───────────────────────────
    # Unlike FGSM which does one big step,
    # BIM starts fresh and takes many small steps
    perturbed_image = image_tensor.clone().detach()


    # ── Step 3: Iteratively apply small FGSM steps ──────────────────────
    for i in range(iterations):

        # Enable gradients for this iteration
        perturbed_image.requires_grad_(True)

        # Forward pass
        output = model(perturbed_image)
        loss = loss_fn(output, true_label)

        # Backward pass
        model.zero_grad()
        loss.backward()

        # Take a small step in gradient sign direction
        # alpha is smaller than epsilon — many small steps
        with torch.no_grad():
            step = alpha * perturbed_image.grad.data.sign()
            perturbed_image = perturbed_image + step

            # ── Clip to epsilon ball ─────────────────────────────────────
            # This ensures total perturbation never exceeds epsilon
            # keeping the attack imperceptible
            perturbation = perturbed_image - image_tensor
            perturbation = torch.clamp(perturbation, -epsilon, epsilon)
            perturbed_image = image_tensor + perturbation

            # Keep pixel values valid
            perturbed_image = torch.clamp(perturbed_image, 0, 1)
            perturbed_image = perturbed_image.detach()


    # ── Step 4: Get final adversarial prediction ─────────────────────────
    with torch.no_grad():
        adversarial_output = model(perturbed_image)
        adversarial_probs = torch.softmax(adversarial_output, dim=1)
        adversarial_pred = adversarial_output.argmax(dim=1).item()
        adversarial_conf = adversarial_probs[0][adversarial_pred].item()

    attack_succeeded = (adversarial_pred != original_pred)
    final_perturbation = perturbed_image - image_tensor

    return {
        "success": attack_succeeded,
        "adversarial_image": perturbed_image,
        "original_pred": original_pred,
        "adversarial_pred": adversarial_pred,
        "original_conf": round(original_conf * 100, 2),
        "adversarial_conf": round(adversarial_conf * 100, 2),
        "perturbation": final_perturbation,
        "epsilon": epsilon,
        "iterations": iterations,
    }
