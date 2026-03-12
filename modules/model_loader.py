import torch
import tempfile
import os
from pathlib import Path


def load_model(uploaded_file):
    """
    Takes the uploaded file from Streamlit,
    saves it temporarily and loads it as a PyTorch model.
    Returns a dict with model info or an error message.
    """

    # ── Step 1: Save uploaded file to a temp location ──────────────────
    # PyTorch needs a real file path to load from
    # so we save the uploaded bytes to a temporary file
    try:
        suffix = Path(uploaded_file.name).suffix  # gets .pt or .pth
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name  # e.g. C:\Users\...\tmpXYZ.pth
    except Exception as e:
        return {"success": False, "error": f"Could not save file: {e}"}


    # ── Step 2: Load with PyTorch ───────────────────────────────────────
    # weights_only=False allows full model loading
    # map_location="cpu" ensures it loads even without a GPU
    try:
        loaded = torch.load(tmp_path, map_location="cpu", weights_only=False)
    except Exception as e:
        os.unlink(tmp_path)  # delete temp file on failure
        return {"success": False, "error": f"Could not load model: {e}"}


    # ── Step 3: Detect what type of file was uploaded ──────────────────
    # Type 1 — Full model (the entire model object was saved)
    # Type 2 — State dict (only the weights were saved, no architecture)
    if isinstance(loaded, dict):
        # It's a state dict — we can't run attacks without architecture
        os.unlink(tmp_path)
        return {
            "success": False,
            "error": "This looks like a state dict (weights only). "
                     "Please upload a full model saved with torch.save(model, path)"
        }

    # ── Step 4: Make sure it has a forward pass ─────────────────────────
    # Without a forward pass we can't run any attacks
    if not callable(getattr(loaded, "forward", None)):
        os.unlink(tmp_path)
        return {"success": False, "error": "Uploaded file is not a valid PyTorch model"}


    # ── Step 5: Put model in eval mode ──────────────────────────────────
    # Eval mode disables dropout and batchnorm training behavior
    # Always required before running inference or attacks
    model = loaded
    model.eval()


    # ── Step 6: Extract model information ───────────────────────────────
    # Count total parameters
    total_params = sum(p.numel() for p in model.parameters())

    # Get all layer names
    layer_names = [name for name, _ in model.named_modules() if name != ""]

    # Count trainable vs frozen parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)


    # ── Step 7: Detect input size ────────────────────────────────────────
    # Try common image sizes to figure out what input the model expects
    input_size = None
    num_classes = None

    for size in [224, 32, 64, 128]:
        try:
            dummy = torch.randn(1, 3, size, size)  # batch of 1, RGB, size x size
            with torch.no_grad():
                output = model(dummy)
            input_size = size
            num_classes = output.shape[1]
            break  # stop once we find a working size
        except:
            continue  # try next size


    # ── Step 8: Clean up temp file ───────────────────────────────────────
    os.unlink(tmp_path)


    # ── Step 9: Return everything ────────────────────────────────────────
    return {
        "success": True,
        "model": model,
        "total_params": total_params,
        "trainable_params": trainable_params,
        "layer_names": layer_names,
        "num_layers": len(layer_names),
        "input_size": input_size,
        "num_classes": num_classes,
    }


def format_param_count(n):
    """
    Converts raw parameter count to readable format
    e.g. 25557032 → '25.6M'
    """
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)