import torch
import torch.nn.functional as F
import numpy as np


def apply_smoothing(image_tensor, method="gaussian", strength="medium"):
    """
    Applies input smoothing to an image tensor as a defense against
    adversarial perturbations. Smoothing disrupts small pixel-level
    perturbations added by attacks like FGSM and BIM.

    Arguments:
        image_tensor -- torch tensor of shape (1, 3, H, W)
        method       -- "gaussian" | "median" | "bilateral"
        strength     -- "low" | "medium" | "high"

    Returns:
        smoothed tensor of same shape
    """

    strength_params = {
        "low":    {"kernel_size": 3, "sigma": 0.5},
        "medium": {"kernel_size": 5, "sigma": 1.0},
        "high":   {"kernel_size": 7, "sigma": 2.0},
    }

    params = strength_params.get(strength, strength_params["medium"])

    if method == "gaussian":
        return _gaussian_smooth(image_tensor, **params)
    elif method == "median":
        return _median_smooth(image_tensor, params["kernel_size"])
    elif method == "bilateral":
        return _bilateral_smooth(image_tensor, **params)
    else:
        return image_tensor


def evaluate_smoothing_defense(model, image_tensor, adversarial_tensor, strength="medium"):
    """
    Evaluates how well smoothing defends against an adversarial example.

    Runs the original and adversarial images through the model both
    with and without smoothing applied, and reports whether smoothing
    recovered the correct prediction.

    Returns a dict:
        {
            "original_pred":            int,
            "adversarial_pred":         int,
            "smoothed_original_pred":   int,
            "smoothed_adversarial_pred":int,
            "defense_success":          bool,
            "confidence_recovery":      float,  # how much confidence recovered
            "method":                   str,
            "strength":                 str
        }
    """
    model.eval()

    with torch.no_grad():

        # ── Baseline predictions ──────────────────────────────────────────
        orig_out  = model(image_tensor)
        adv_out   = model(adversarial_tensor)

        orig_pred = int(orig_out.argmax(dim=1).item())
        adv_pred  = int(adv_out.argmax(dim=1).item())
        adv_conf  = float(torch.softmax(adv_out, dim=1).max().item()) * 100

        # ── Smoothed predictions ──────────────────────────────────────────
        smoothed_orig = apply_smoothing(image_tensor,     method="gaussian", strength=strength)
        smoothed_adv  = apply_smoothing(adversarial_tensor, method="gaussian", strength=strength)

        s_orig_out  = model(smoothed_orig)
        s_adv_out   = model(smoothed_adv)

        s_orig_pred = int(s_orig_out.argmax(dim=1).item())
        s_adv_pred  = int(s_adv_out.argmax(dim=1).item())
        s_adv_conf  = float(torch.softmax(s_adv_out, dim=1).max().item()) * 100

        # Defense succeeds if smoothing restores the original prediction
        defense_success    = (s_adv_pred == orig_pred)
        conf_recovery      = round(s_adv_conf - adv_conf, 2)

    return {
        "original_pred":             orig_pred,
        "adversarial_pred":          adv_pred,
        "smoothed_original_pred":    s_orig_pred,
        "smoothed_adversarial_pred": s_adv_pred,
        "defense_success":           defense_success,
        "confidence_recovery":       conf_recovery,
        "method":                    "gaussian",
        "strength":                  strength
    }


# ── Smoothing implementations ─────────────────────────────────────────────

def _gaussian_smooth(tensor, kernel_size=5, sigma=1.0):
    """
    Applies Gaussian blur to each channel independently.
    Most effective against high-frequency adversarial noise (FGSM, BIM).
    """
    kernel = _gaussian_kernel(kernel_size, sigma)
    kernel = kernel.unsqueeze(0).unsqueeze(0)  # (1, 1, K, K)

    channels = tensor.shape[1]
    kernel   = kernel.repeat(channels, 1, 1, 1)  # (C, 1, K, K)

    padding  = kernel_size // 2
    smoothed = F.conv2d(tensor, kernel, padding=padding, groups=channels)

    return torch.clamp(smoothed, 0, 1)


def _median_smooth(tensor, kernel_size=5):
    """
    Applies median filtering by unfolding patches and taking the median.
    More aggressive than Gaussian — better against salt-and-pepper noise.
    """
    padding  = kernel_size // 2
    padded   = F.pad(tensor, [padding] * 4, mode="reflect")

    # Unfold into patches
    patches  = padded.unfold(2, kernel_size, 1).unfold(3, kernel_size, 1)
    # patches shape: (B, C, H, W, K, K)

    # Take median over the patch dimensions
    smoothed = patches.contiguous().view(*patches.shape[:4], -1).median(dim=-1).values

    return torch.clamp(smoothed, 0, 1)


def _bilateral_smooth(tensor, kernel_size=5, sigma=1.0):
    """
    Simplified bilateral filter — preserves edges better than Gaussian
    while still suppressing adversarial noise.
    Uses a spatial Gaussian weighted by intensity similarity.
    """
    padding  = kernel_size // 2
    padded   = F.pad(tensor, [padding] * 4, mode="reflect")

    B, C, H, W = tensor.shape
    result      = torch.zeros_like(tensor)

    spatial_kernel = _gaussian_kernel(kernel_size, sigma)

    for i in range(kernel_size):
        for j in range(kernel_size):
            neighbor    = padded[:, :, i:i+H, j:j+W]
            # Intensity weight: pixels similar in value get higher weight
            intensity_w = torch.exp(-((tensor - neighbor) ** 2) / (2 * sigma ** 2))
            spatial_w   = spatial_kernel[i, j]
            result      += spatial_w * intensity_w * neighbor

    # Normalise
    norm_factor = torch.ones_like(tensor)
    for i in range(kernel_size):
        for j in range(kernel_size):
            neighbor    = padded[:, :, i:i+H, j:j+W]
            intensity_w = torch.exp(-((tensor - neighbor) ** 2) / (2 * sigma ** 2))
            spatial_w   = spatial_kernel[i, j]
            norm_factor += spatial_w * intensity_w

    result = result / (norm_factor + 1e-8)
    return torch.clamp(result, 0, 1)


def _gaussian_kernel(size, sigma):
    """
    Creates a 2D Gaussian kernel of given size and sigma.
    """
    coords = torch.arange(size, dtype=torch.float32) - size // 2
    grid   = torch.stack(torch.meshgrid(coords, coords, indexing="ij"), dim=-1)
    kernel = torch.exp(-(grid ** 2).sum(dim=-1) / (2 * sigma ** 2))
    kernel = kernel / kernel.sum()
    return kernel