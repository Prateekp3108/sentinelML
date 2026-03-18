from groq import Groq
import streamlit as st

def _get_client():
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in secrets")
    return Groq(api_key=api_key)


# ── Tier-aware prompts ────────────────────────────────────────────────────
TIER_PROMPTS = {
    "student": """
You are a friendly ML security teacher explaining results to a beginner student.

Given the audit results and model source code below, provide:
1. A simple plain-English explanation of what the vulnerabilities mean (no jargon)
2. Why this matters in real life (give a simple example)
3. 3 beginner-friendly suggestions to make the model safer
4. Encouragement and next steps for learning

Keep it conversational, supportive, and under 400 words.
Avoid technical terms — if you must use one, explain it immediately.
""",

    "engineer": """
You are a senior ML security engineer reviewing a model audit report.

Given the audit results and model source code below, provide:
1. Technical analysis of each vulnerability found (reference specific attack results)
2. Exact code changes needed — show before/after code snippets
3. Specific defense strategies: adversarial training parameters, input preprocessing recommendations
4. Architecture-level suggestions based on the detected layer structure
5. Priority order for fixes (critical → high → medium)

Be precise, technical, and actionable. Reference specific layers and parameters where relevant.
Keep it under 600 words.
""",

    "redteam": """
You are a red team ML security researcher writing a formal threat assessment.

Given the audit results and model source code below, provide:
1. Full threat model — what attack scenarios this model is vulnerable to in deployment
2. Rewrite the ENTIRE model source code with all security fixes applied
   - Add adversarial training loop
   - Add input preprocessing defenses
   - Add randomized smoothing wrapper
   - Add MRR (Modular Robust Redundancy) inference
   - Add inline comments explaining every security change
3. CVE-style vulnerability descriptions for each finding
4. Deployment recommendations and monitoring strategy

Be exhaustive. The rewritten code must be complete and runnable.
"""
}


def build_audit_summary(model_result, attack_results=None, trojan_results=None):
    """
    Builds a structured text summary of the audit results
    to pass as context to the AI.
    """
    lines = []

    # ── Model info ────────────────────────────────────────────────────────
    from modules.model_loader import format_param_count
    lines.append("=== MODEL INFORMATION ===")
    lines.append(f"Total Parameters: {format_param_count(model_result.get('total_params', 0))}")
    lines.append(f"Total Layers: {model_result.get('num_layers', '?')}")
    lines.append(f"Output Classes: {model_result.get('num_classes', '?')}")
    lines.append(f"Input Size: {model_result.get('input_size', '?')}px")

    layer_names = model_result.get("layer_names", [])
    if layer_names:
        lines.append(f"Layer Types: {', '.join(set(n.split('(')[0] for n in layer_names[:20]))}")

    # ── Adversarial results ───────────────────────────────────────────────
    if attack_results:
        lines.append("\n=== ADVERSARIAL ATTACK RESULTS ===")
        score = attack_results.get("robustness_score", 0)
        lines.append(f"Overall Robustness Score: {score}/100")

        attack_meta = {
            "fgsm":     "FGSM (Fast Gradient Sign Method — one-step, easy attack)",
            "bim":      "BIM (Basic Iterative Method — 10 iterations, medium attack)",
            "deepfool": "DeepFool (minimum perturbation — hardest attack)",
        }

        for key, desc in attack_meta.items():
            r = attack_results.get(key, {})
            if "error" in r:
                lines.append(f"{desc}: ERROR — {r['error']}")
            elif r.get("success"):
                orig = r.get("original_conf", "?")
                adv  = r.get("adversarial_conf", "?")
                lines.append(f"{desc}: VULNERABLE — confidence dropped {orig}% → {adv}%")
            else:
                lines.append(f"{desc}: RESISTED")

    # ── Trojan results ────────────────────────────────────────────────────
    if trojan_results and not trojan_results.get("error"):
        lines.append("\n=== TROJAN / BACKDOOR DETECTION ===")
        detected = trojan_results.get("trojan_detected", False)
        lines.append(f"Trojan Detected: {'YES' if detected else 'NO'}")
        lines.append(f"Anomaly Index: {trojan_results.get('anomaly_index', 0)}")
        lines.append(f"Detection Confidence: {trojan_results.get('confidence', 'N/A')}")
        if detected:
            lines.append(f"Suspected Target Class: {trojan_results.get('suspected_target_class')}")
        lines.append(f"Classes Scanned: {trojan_results.get('classes_scanned', 0)}")

    return "\n".join(lines)


def call_gemini(audit_summary, source_code, tier, status_callback=None):
    """
    Calls Gemini API with tier-aware prompt and returns the response text.

    Arguments:
        audit_summary  -- string from build_audit_summary()
        source_code    -- string content of uploaded .py file
        tier           -- "student" | "engineer" | "redteam"
        status_callback -- optional function(msg) for progress updates

    Returns:
        str — AI response text
    """

    def update(msg):
        if status_callback:
            status_callback(msg)

    try:
        update("Connecting to Gemini...")
        model = _get_client()

        tier_prompt = TIER_PROMPTS.get(tier, TIER_PROMPTS["engineer"])

        prompt = f"""
{tier_prompt}

{audit_summary}

=== MODEL SOURCE CODE ===
{source_code}

Please provide your analysis now.
"""

        update("Analyzing vulnerabilities...")
        client = _get_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.3
        )

        update("Generating recommendations...")
        return response.choices[0].message.content

    except Exception as e:
        return f"AI analysis failed: {str(e)}"


def call_gemini_no_code(audit_summary, tier, status_callback=None):
    """
    Same as call_gemini but without source code —
    used when user hasn't uploaded a .py file.
    Gives general recommendations based on audit results only.
    """

    def update(msg):
        if status_callback:
            status_callback(msg)

    try:
        update("Connecting to Gemini...")
        model = _get_client()

        tier_prompt = TIER_PROMPTS.get(tier, TIER_PROMPTS["engineer"])

        prompt = f"""
{tier_prompt}

{audit_summary}

=== MODEL SOURCE CODE ===
No source code was provided. Base your recommendations on the audit results
and the detected architecture information above. Give general but actionable advice.

Please provide your analysis now.
"""

        update("Analyzing audit results...")
        update("Analyzing vulnerabilities...")
        client = _get_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.3
        )

        update("Generating recommendations...")
        return response.choices[0].message.content

    except Exception as e:
        return f"AI analysis failed: {str(e)}"