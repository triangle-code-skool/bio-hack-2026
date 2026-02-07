UltraViab — MVP Build Plan
3-Person Team: 2 CS Majors, 1 BME Student
BioHack 2026 | ~24 hours | Deadline: Sunday 11 AM

TEAM ROLES AT A GLANCE
Role
Person
Primary Responsibility
Key Deliverables
BME
—
Clinical Lead, Data Architect, Pitch Owner
Feature spec, synthetic dataset, clinical validation, pitch deck, workflow diagrams
CS #1
—
ML Pipeline & Backend
Trained model, API/function, evaluation plots
CS #2
—
Frontend, Integration & Demo
Streamlit/React dashboard, visual design, live demo
With only one BME, that person carries both the clinical authority AND the pitch narrative. The tradeoff is they can't also own a 3D print or deep visual design work — so the CS students need to pick up more of the visual/presentation polish. The plan below is designed to keep the BME focused on the two things only they can do: clinical accuracy and telling the story to judges.

BME — "Clinical Lead, Data Architect & Pitch Owner"
You're the most versatile and most time-pressured person on the team. You own three things no one else can do: defining clinically accurate parameters, validating model outputs, and selling the story to judges. Everything else gets delegated.
Hour 0–1: Define the Feature Space
This is your first and most urgent deliverable — CS #1 is blocked until you hand this off. You're answering: "If we had a magic ultrasound probe on a donor organ, what numbers would we read, and what do they mean?"
Primary ultrasound-derived features (model inputs):
Feature
Unit
Normal Range
Abnormal Range
Source/Rationale
Tissue stiffness (Young's modulus)
kPa
3.8–6.0 (liver)
>12 = significant fibrosis, >27 = acute failure
Science Advances 2024, SWE literature
Resistive index (RI)
dimensionless
0.5–0.7
>0.8 = abnormal arterial resistance
Di Martino et al., multiple Doppler studies
Shear wave velocity
m/s
1.8–2.2 (kidney cortex)
>2.6 = elevated stiffness, worse outcomes
PMC 2023, OR=17.1 for adverse outcomes
Perfusion uniformity score
0–100%
>85% = uniform
<60% = significant perfusion defects
CEUS pancreas study, conceptual
Echogenicity grade
1–5 scale
1–2 = homogeneous
4–5 = heterogeneous/concerning
B-mode assessment standards
Edema index
0–10 scale
0–3
>6 = significant tissue swelling
Derived from parenchymal assessment
Donor/clinical metadata features:
Feature
Unit
Range
Notes
Cold ischemia time (CIT)
hours
0–40+
Kidney: 24–36h tolerance; Liver: 12–18h; Heart: ~4h
Organ type
categorical
kidney, liver, heart, lung
Different thresholds per organ
Donor age
years
0–80
Older donors = higher baseline risk
KDPI (kidneys) / DRI (livers)
percentile/score
0–100
Donor quality index
Donor cause of death
categorical
trauma, CVA, anoxia, other
Affects organ quality
Warm ischemia time
minutes
0–60
Especially important for DCD organs
Deliverable: A clean table (markdown, Google Sheet, whatever is fastest) with every feature, its unit, range, clinical meaning, and threshold for concern. Send to CS #1 by end of Hour 1. Do not perfectionate this — good enough now beats perfect at Hour 3.
Hour 1–3: Build the Synthetic Training Dataset (pair with CS #1)
This is your most critical task. Sit next to CS #1 for this. You provide the clinical logic; they write the Python. You should NOT be wrestling with pandas alone — that's a waste of your domain expertise.
What you define, what CS #1 codes:
You say: "A viable kidney has stiffness 3–6 kPa, RI 0.5–0.65, CIT under 20h, donor age under 55, KDPI under 60. Add gaussian noise with σ = 0.5 for stiffness, 0.05 for RI."
CS #1 types: stiffness = np.random.normal(4.5, 0.5, n_viable_kidneys)
You say: "Non-viable organs should have correlated abnormalities — high stiffness AND high RI AND long CIT tend to cluster together, not appear independently."
CS #1 implements the correlation structure.
Outcome labels (what the model predicts):
    •    Accept (viable) — Score 70–100. Healthy parameters, good graft function expected.
    •    Marginal (inspect further) — Score 40–69. Some concerning features, potentially transplantable.
    •    Decline (non-viable) — Score 0–39. Multiple red flags, high graft failure risk.
Target: 500–1000 rows, ~40% Accept, ~35% Marginal, ~25% Decline (reflects real-world skew — most recovered organs are at least considered).
Deliverable: training_data.csv handed to CS #1 by Hour 3. You keep a copy to reference during validation.
Hour 3–4: Clinical Workflow Diagram
While CS #1 trains the model, you create the workflow diagram showing where UltraViab fits in the transplant pipeline. Use whatever tool is fastest — PowerPoint, Canva, draw.io, Google Slides, or even hand-drawn + photographed.
The flow: