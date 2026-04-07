# SENTINEL(ML)

An ML Model Security Auditor — detect adversarial vulnerabilities and neural Trojan backdoors in your PyTorch models.

## What it does

SentinelML automatically tests your trained PyTorch models against three classes of attacks and generates a full security report:

- **Adversarial Attack Testing** — runs FGSM, BIM, and DeepFool attacks and scores your model's robustness (0–100)
- **Neural Trojan Detection** — uses Neural Cleanse with MAD anomaly scoring to detect hidden backdoor triggers
- **AI Security Analysis** — powered by Llama 3.3 70B via Groq, generates tier-aware recommendations and can rewrite vulnerable model code
- **PDF Report Export** — downloadable audit report with scores, verdicts, and layer architecture

## Live Demo

[sentinelml.streamlit.app](https://sentinelml.streamlit.app)

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend & Backend | Python, Streamlit |
| ML Framework | PyTorch, TorchVision |
| Attack Suite | FGSM, BIM, DeepFool (custom implementations) |
| Defense Layer | Gaussian/Median/Bilateral smoothing, MRR |
| Trojan Detection | Neural Cleanse, activation clustering |
| AI Analysis | Llama 3.3 70B via Groq API |
| Auth | GitHub OAuth via streamlit-oauth |
| Report Generation | ReportLab |
| Deployment | Streamlit Community Cloud |

## Getting Started

**Requirements:** Python 3.10+
```
bash
git clone https://github.com/Prateekp3108/sentinelML.git
cd sentinelML
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```
toml
GITHUB_CLIENT_ID = "your_client_id"
GITHUB_CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:8501"
GROQ_API_KEY = "your_groq_key"
```

Run:
```
bash
streamlit run app.py
```

## Generating a Test Model
```
python
import torch
import torchvision.models as models

model = models.resnet18(weights='IMAGENET1K_V1')
torch.save(model, 'sample_models/resnet18.pth')
```

Upload the `.pth` file on the audit page to run a full security scan.

## User Tiers

After login, users select an experience tier that shapes the AI analysis:

| Tier | Gets |
|---|---|
| 🟢 Student / Researcher | Plain English explanation of vulnerabilities |
| 🔵 ML Engineer | Technical breakdown + specific code fixes |
| 🔴 Red Team Analyst | Full rewritten model code + threat model |

## Research Basis

Built on two research papers:

- *Safe Machine Learning and Defeating Adversarial Attacks* — MRR defense methodology
- *A Survey on Neural Trojans* — Neural Cleanse detection, activation clustering

## Developers

**Prateek Pandey** — Manipal University Jaipur · [github.com/Prateekp3108](https://github.com/Prateekp3108)

**Suhani Sharma** — Manipal University Jaipur · [github.com/tsunamiuwu](https://github.com/tsunamiuwu)
