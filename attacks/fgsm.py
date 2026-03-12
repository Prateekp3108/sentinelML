import torch
import torch.nn as nn


def fgsm_attack(model, image_tensor, true_label, epsilon=0.1):
    """
    Fast Gradient Sign Method (FGSM) attack.
    
    Arguments:
        model         -- the victim PyTorch model
        image_tensor  -- input image as tensor, shape (1, 3, H, W)
        true_label    -- the correct class index as a tensor
        epsilon       -- attack strength (0.0 to 1.0), higher = stronger attack
    
    Returns a dict with:
        success          -- whether the attack fooled the model
        adversarial_image -- the perturbed image tensor
        original_pred    -- what the model predicted on clean image
        adversarial_pred -- what the model predicted on adversarial image
        original_conf    -- confidence on clean image
        adversarial_conf -- confidence on adversarial image
        perturbation     -- the noise that was added
    """

    model.eval()
    loss_fn = nn.CrossEntropyLoss()

    # ── Step 1: Get original prediction ─────────────────────────────────
    # Run the clean image through the model first
    # so we can compare before vs after the attack
    with torch.no_grad():
        original_output = model(image_tensor)
        original_probs = torch.softmax(original_output, dim=1)
        original_pred = original_output.argmax(dim=1).item()
        original_conf = original_probs[0][original_pred].item()


    # ── Step 2: Enable gradients on the image ───────────────────────────
    # Normally gradients are computed for model weights
    # In FGSM we compute gradients for the INPUT IMAGE instead
    # This tells us which pixels to change to maximally increase the loss
    perturbed_image = image_tensor.clone().detach().requires_grad_(True)


    # ── Step 3: Forward pass ─────────────────────────────────────────────
    output = model(perturbed_image)
    loss = loss_fn(output, true_label)


    # ── Step 4: Backward pass ────────────────────────────────────────────
    # Compute gradient of loss with respect to the image
    # model.zero_grad() clears any leftover gradients from previous runs
    model.zero_grad()
    loss.backward()


    # ── Step 5: Create perturbation ──────────────────────────────────────
    # Take the SIGN of the gradient (just +1 or -1 per pixel)
    # Multiply by epsilon to control how strong the attack is
    # This is the core FGSM formula:
    # adversarial = image + epsilon * sign(gradient)
    gradient_sign = perturbed_image.grad.data.sign()
    perturbation = epsilon * gradient_sign


    # ── Step 6: Apply perturbation ───────────────────────────────────────
    # Add the perturbation to the original image
    # Clamp to [0,1] to keep pixel values valid
    adversarial_image = image_tensor + perturbation
    adversarial_image = torch.clamp(adversarial_image, 0, 1)


    # ── Step 7: Get adversarial prediction ──────────────────────────────
    # Run the perturbed image through the model
    # to see if the attack succeeded
    with torch.no_grad():
        adversarial_output = model(adversarial_image)
        adversarial_probs = torch.softmax(adversarial_output, dim=1)
        adversarial_pred = adversarial_output.argmax(dim=1).item()
        adversarial_conf = adversarial_probs[0][adversarial_pred].item()


    # ── Step 8: Return results ───────────────────────────────────────────
    attack_succeeded = (adversarial_pred != original_pred)

    return {
        "success": attack_succeeded,
        "adversarial_image": adversarial_image.detach(),
        "original_pred": original_pred,
        "adversarial_pred": adversarial_pred,
        "original_conf": round(original_conf * 100, 2),
        "adversarial_conf": round(adversarial_conf * 100, 2),
        "perturbation": perturbation.detach(),
        "epsilon": epsilon,
    }
