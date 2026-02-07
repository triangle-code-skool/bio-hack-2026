# UltraViab — MVP Build Plan
## 3-Person Team: 2 CS Majors, 1 BME Student
### BioHack 2026 | ~24 hours | Deadline: Sunday 11 AM

---

## TEAM ROLES AT A GLANCE

| Role | Person | Primary Responsibility | Key Deliverables |
|------|--------|----------------------|------------------|
| **BME** | — | Clinical Lead, Data Architect, Pitch Owner | Feature spec, synthetic dataset, clinical validation, pitch deck, workflow diagrams |
| **CS #1** | — | ML Pipeline & Backend | Trained model, API/function, evaluation plots |
| **CS #2** | — | Frontend, Integration & Demo | Streamlit/React dashboard, visual design, live demo |

With only one BME, that person carries both the clinical authority AND the pitch narrative. The tradeoff is they can't also own a 3D print or deep visual design work — so the CS students need to pick up more of the visual/presentation polish. The plan below is designed to keep the BME focused on the two things only they can do: **clinical accuracy** and **telling the story to judges**.

---

## BME — "Clinical Lead, Data Architect & Pitch Owner"

You're the most versatile and most time-pressured person on the team. You own three things no one else can do: defining clinically accurate parameters, validating model outputs, and selling the story to judges. Everything else gets delegated.

### Hour 0–1: Define the Feature Space

This is your first and most urgent deliverable — **CS #1 is blocked until you hand this off.** You're answering: "If we had a magic ultrasound probe on a donor organ, what numbers would we read, and what do they mean?"

**Primary ultrasound-derived features (model inputs):**

| Feature | Unit | Normal Range | Abnormal Range | Source/Rationale |
|---------|------|-------------|----------------|-----------------|
| Tissue stiffness (Young's modulus) | kPa | 3.8–6.0 (liver) | >12 = significant fibrosis, >27 = acute failure | Science Advances 2024, SWE literature |
| Resistive index (RI) | dimensionless | 0.5–0.7 | >0.8 = abnormal arterial resistance | Di Martino et al., multiple Doppler studies |
| Shear wave velocity | m/s | 1.8–2.2 (kidney cortex) | >2.6 = elevated stiffness, worse outcomes | PMC 2023, OR=17.1 for adverse outcomes |
| Perfusion uniformity score | 0–100% | >85% = uniform | <60% = significant perfusion defects | CEUS pancreas study, conceptual |
| Echogenicity grade | 1–5 scale | 1–2 = homogeneous | 4–5 = heterogeneous/concerning | B-mode assessment standards |
| Edema index | 0–10 scale | 0–3 | >6 = significant tissue swelling | Derived from parenchymal assessment |

**Donor/clinical metadata features:**

| Feature | Unit | Range | Notes |
|---------|------|-------|-------|
| Cold ischemia time (CIT) | hours | 0–40+ | Kidney: 24–36h tolerance; Liver: 12–18h; Heart: ~4h |
| Organ type | categorical | kidney, liver, heart, lung | Different thresholds per organ |
| Donor age | years | 0–80 | Older donors = higher baseline risk |
| KDPI (kidneys) / DRI (livers) | percentile/score | 0–100 | Donor quality index |
| Donor cause of death | categorical | trauma, CVA, anoxia, other | Affects organ quality |
| Warm ischemia time | minutes | 0–60 | Especially important for DCD organs |

**Deliverable:** A clean table (markdown, Google Sheet, whatever is fastest) with every feature, its unit, range, clinical meaning, and threshold for concern. **Send to CS #1 by end of Hour 1. Do not perfectionate this — good enough now beats perfect at Hour 3.**

### Hour 1–3: Build the Synthetic Training Dataset (pair with CS #1)

This is your most critical task. **Sit next to CS #1 for this.** You provide the clinical logic; they write the Python. You should NOT be wrestling with pandas alone — that's a waste of your domain expertise.

**What you define, what CS #1 codes:**

You say: "A viable kidney has stiffness 3–6 kPa, RI 0.5–0.65, CIT under 20h, donor age under 55, KDPI under 60. Add gaussian noise with σ = 0.5 for stiffness, 0.05 for RI."

CS #1 types: `stiffness = np.random.normal(4.5, 0.5, n_viable_kidneys)`

You say: "Non-viable organs should have correlated abnormalities — high stiffness AND high RI AND long CIT tend to cluster together, not appear independently."

CS #1 implements the correlation structure.

**Outcome labels (what the model predicts):**
- **Accept (viable)** — Score 70–100. Healthy parameters, good graft function expected.
- **Marginal (inspect further)** — Score 40–69. Some concerning features, potentially transplantable.
- **Decline (non-viable)** — Score 0–39. Multiple red flags, high graft failure risk.

**Target: 500–1000 rows, ~40% Accept, ~35% Marginal, ~25% Decline** (reflects real-world skew — most recovered organs are at least considered).

**Deliverable:** `training_data.csv` handed to CS #1 by Hour 3. You keep a copy to reference during validation.

### Hour 3–4: Clinical Workflow Diagram

While CS #1 trains the model, you create the workflow diagram showing where UltraViab fits in the transplant pipeline. Use whatever tool is fastest — PowerPoint, Canva, draw.io, Google Slides, or even hand-drawn + photographed.

**The flow:**
```
Donor Identified → Family Authorization → Organ Recovery
                                              ↓
                                    ┌─────────────────────┐
                                    │  ★ UltraViab SCAN ★ │
                                    │  Portable US probe   │
                                    │  applied to organ    │
                                    │  → Viability score   │
                                    │    transmitted to    │
                                    │    accepting center  │
                                    └─────────────────────┘
                                              ↓
                              Match Run → Offer Cascade → Accept/Decline
                                              ↓
                                    Transport → Transplant
```

Show that the scan happens **at the donor hospital during/after recovery** and the score is sent digitally to potential accepting centers as part of the offer package. This replaces or supplements the current subjective visual inspection.

**Deliverable:** One clean diagram image. Send to CS #2 to embed in the dashboard, and keep for the pitch deck.

### Hour 4–6: Validate the Model + Start Pitch Deck

**Validation (30–45 min):** CS #1 has a trained model by now. Test it with edge cases:

| Test Case | Expected Result | Why It Matters |
|-----------|----------------|----------------|
| Young donor, 6h CIT, all normal US | Accept (85+) | Sanity check — obvious good organ |
| 70-year-old donor, 32h CIT, stiffness 15 kPa | Decline (<30) | Sanity check — obvious bad organ |
| KDPI = 95 but excellent US features | Marginal (50–65) | Key story: US data can rescue organs the KDPI alone would reject |
| Great donor profile but stiffness = 20 kPa | Decline (25–35) | US catches damage that donor demographics miss |
| 14h CIT liver, borderline RI of 0.75 | Marginal (45–55) | Toss-up case — model should flag, not auto-reject |

If the model gets any of these obviously wrong, tell CS #1 which direction to adjust. This is an iterative 15-minute conversation, not a formal report.

**Pitch deck (start building, ~2 hours):** You own the narrative. Build in PowerPoint or Google Slides:

| Slide | Content | Your Notes |
|-------|---------|------------|
| 1 | Title: "UltraViab: Non-Invasive Organ Viability Scoring" | Team name, BioHack 2026, Health Universe logo |
| 2 | **Inspiration** — The 2:47 AM scenario from the Health Universe challenge. Why this problem matters to you. | Personal, brief, emotional hook |
| 3 | **Problem Statement** — 20–30% discard rate, 100K+ waitlist, subjective assessment, biopsy increases discard risk. Cite Dr. Sellers' keynote. | Use 2–3 hard stats. Keep it punchy. |
| 4 | **What It Does** — Portable US probe + ML = objective viability score in minutes. Show workflow diagram. | High level only. "Scan → Score → Decision" |
| 5 | **How We Built It** — Tech stack, feature table, synthetic data approach. | CS #1 provides content, you arrange it |
| 6 | **Live Demo** — CS #2 drives the dashboard. You narrate. | Leave this slide mostly empty — it's a live section |
| 7 | **Technical Results** — ROC curve, confusion matrix, feature importance. | CS #1 provides plots, you contextualize them |
| 8 | **Advantages** — Non-invasive (unlike biopsy). Objective (unlike visual inspection). Fast. Portable. Works with existing US hardware. | Bullet points are fine here |
| 9 | **Challenges & Lessons** — Synthetic data limitations, threshold calibration, organ-specific tuning. What you'd do with real clinical data. | Honesty scores well with judges |
| 10 | **Future Vision** — Integration with machine perfusion, UNOS/OPTN, prospective clinical validation. Health Universe deployment. | End with impact: "Every organ saved = a life saved" |

**Deliverable:** First-draft slide deck by Hour 6. Doesn't need to be pretty yet — structure and content first.

### Hour 6–8: Polish Deck + Prepare Demo Script

- Request screenshots of the working dashboard from CS #2
- Request evaluation plot PNGs from CS #1
- Insert both into the deck
- Write a demo script: exactly which preset scenario to load first, what to point out, what story each scenario tells
- Write brief speaker notes for each slide
- **Assign speaking parts** (see Speaking Parts section below)

### Hour 8+ Saturday / Hour 8–11 Sunday: Rehearse & Submit

- Full team rehearsal: 2–3 runthroughs, timed
- Tighten any slide that runs long
- Export final deck as both PDF and PowerPoint
- Submit to your team's Discord channel before 11 AM Sunday
- Arrive at Fontana 1000 before 11:30 AM

---

## CS #1 — "ML Pipeline & Backend"

You own the brain of UltraViab. Your secondary role is helping the BME build the dataset — don't let them struggle with Python if that's not their strength.

### Hour 0–1: Environment Setup & Pipeline Skeleton

While waiting for the BME's feature spec:

```
ultraviab/
├── data/
│   ├── generate_data.py           # Co-authored with BME
│   └── training_data.csv          # Output
├── model/
│   ├── train.py                   # Training script
│   ├── predict.py                 # Prediction function (CS #2 calls this)
│   ├── evaluate.py                # Metrics & plot generation
│   └── model.pkl                  # Saved trained model
├── app/
│   └── streamlit_app.py           # CS #2 owns this
└── outputs/
    ├── roc_curve.png
    ├── confusion_matrix.png
    └── feature_importance.png
```

- Install: `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `joblib`
- Write the prediction interface immediately (CS #2 needs this to start integrating):

```python
# predict.py — CS #2 imports this
def predict_viability(features: dict) -> dict:
    """
    Input: {organ_type, stiffness, ri, swv, perfusion,
            echogenicity, edema, cit, donor_age, kdpi, ...}
    Output: {score: 0-100, classification: str,
             confidence: 0-1, feature_contributions: dict}
    """
    # PLACEHOLDER — rule-based until model is trained
    score = 100 - (features['stiffness'] * 3) - (features['ri'] * 40) \
            - (features['cit'] * 1.5) - (features['donor_age'] * 0.3)
    score = max(0, min(100, score))
    classification = 'accept' if score >= 70 else 'marginal' if score >= 40 else 'decline'
    return {"score": round(score, 1), "classification": classification,
            "confidence": 0.85, "feature_contributions": {}}
```

**Deliverable:** Working `predict.py` with placeholder logic shared with CS #2 by end of Hour 1.

### Hour 1–3: Co-Build Synthetic Dataset with BME

**Sit with the BME.** They have the clinical knowledge; you have the coding speed. This is a pairing exercise.

**Approach:**

```python
# generate_data.py — skeleton
import numpy as np
import pandas as pd

def generate_organ_data(organ_type, n_accept, n_marginal, n_decline):
    """BME defines the distributions, you code them."""
    rows = []

    # VIABLE ORGANS — BME tells you the normal ranges
    for _ in range(n_accept):
        row = {
            'organ_type': organ_type,
            'stiffness': np.random.normal(mean, std),  # BME fills in mean/std
            'ri': np.random.normal(mean, std),
            'swv': np.random.normal(mean, std),
            'perfusion': np.random.normal(mean, std),
            'echogenicity': np.random.choice([1, 2], p=[0.7, 0.3]),
            'edema': np.random.normal(mean, std),
            'cit': np.random.uniform(low, high),       # BME defines per organ
            'donor_age': np.random.normal(mean, std),
            'kdpi': np.random.normal(mean, std),
            'viability_label': 'accept',
            'viability_score': np.random.uniform(70, 100)
        }
        rows.append(row)

    # MARGINAL and DECLINE — similar but with shifted distributions
    # BME defines HOW they shift (correlated abnormalities)
    ...

    return pd.DataFrame(rows)

# Generate per organ type
kidney_data = generate_organ_data('kidney', 150, 120, 80)
liver_data = generate_organ_data('liver', 130, 110, 90)
heart_data = generate_organ_data('heart', 100, 80, 70)
# ... combine, shuffle, export
```

Key: the BME dictates the numbers, you type fast and handle edge cases (clipping negative values, ensuring correlations, etc.).

**Deliverable:** `training_data.csv` — 500–1000 rows — by Hour 3.

### Hour 3–5: Train the Model

**Primary model: Random Forest Classifier** — fast to train, gives feature importances, handles mixed feature types well.

```python
# train.py
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# Load data
df = pd.read_csv('data/training_data.csv')

# Encode organ_type
df = pd.get_dummies(df, columns=['organ_type'])

# Features and labels
X = df.drop(['viability_label', 'viability_score'], axis=1)
y_class = df['viability_label']   # For classification
y_score = df['viability_score']   # For regression

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train classifier (accept / marginal / decline)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(clf, X_scaled, y_class, cv=5, scoring='f1_macro')
print(f"5-fold F1: {scores.mean():.3f} ± {scores.std():.3f}")
clf.fit(X_scaled, y_class)

# Train regressor (continuous 0-100 score)
reg = GradientBoostingRegressor(n_estimators=100, random_state=42)
reg.fit(X_scaled, y_score)

# Save everything
joblib.dump({'clf': clf, 'reg': reg, 'scaler': scaler,
             'feature_names': list(X.columns)}, 'model/model.pkl')
```

**Deliverable by Hour 5:** Trained model saved to `model.pkl`. Update `predict.py` to load and use the real model instead of placeholder logic. Tell CS #2 it's ready.

### Hour 5–6: Evaluation Plots

Generate three key images for the pitch deck:

1. **ROC Curve** — Per-class (accept vs. rest, marginal vs. rest, decline vs. rest) with AUC. Use `sklearn.metrics.RocCurveDisplay`.

2. **Confusion Matrix** — Heatmap via seaborn. Judges want to see that the model rarely classifies "Accept" organs as "Decline" (worst failure mode = discarding a viable organ).

3. **Feature Importance** — `clf.feature_importances_` plotted as horizontal bar chart, sorted descending, color-coded (blue = ultrasound features, gray = donor metadata). **This is your most important plot** — it tells the story "ultrasound tissue stiffness is 2x more predictive than donor age alone, which is why acoustic assessment adds value."

Optional if time permits:
4. **Sensitivity curves** — Sweep CIT from 0–40h while holding other features at "normal" values, plot how the viability score degrades. Do this per organ type. Shows the "degradation curve" concept.

**Deliverable:** PNG exports of all plots, sent to BME for the pitch deck.

### Hour 6–8: Validation Loop + Edge Case Hardening

- Work with BME on their test cases (see BME Hour 4–6 section)
- Add input validation to `predict.py` (clip out-of-range values, handle missing inputs gracefully)
- Make sure `predict_viability()` returns reasonable `feature_contributions` — these drive CS #2's contribution bar chart
- If time: add SHAP values for explainability (very impressive for judges but not essential)

### Sunday Morning: Bug Fixes & Demo Support
- Be on standby for any backend issues during rehearsal
- Export final model performance numbers (accuracy, F1) for the BME to cite during the pitch
- Help CS #2 with any last-minute integration issues

---

## CS #2 — "Frontend, Visual Design & Demo Lead"

You own what the judges actually see. A working, beautiful demo wins hackathons. Your secondary role is picking up visual/design tasks that would normally fall to a second BME — things like making the dashboard look clinical and professional, and helping polish the pitch deck visuals.

### Hour 0–2: Dashboard Skeleton with Placeholder Data

**Don't wait for anyone.** Start building the UI now with hardcoded values using CS #1's placeholder `predict.py`.

**Recommended stack:** Streamlit (fastest for a hackathon — built-in sliders, columns, charts). Use React only if you're confident you can have a working app in 4 hours.

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│  🔬 UltraViab — Non-Invasive Organ Viability Assessment      │
│  [Kidney ▼]    Scan ID: UV-2026-0207    02:47 AM EST        │
├────────────────┬──────────────────┬──────────────────────────┤
│ SCAN INPUTS    │ VIABILITY RESULT │ PARAMETER ANALYSIS       │
│                │                  │                          │
│ Organ Type     │      ┌───┐      │ ┌──────────────────────┐ │
│ [Kidney    ▼]  │      │78 │      │ │   Radar/Spider Chart │ │
│                │      └───┘      │ │   - each param axis  │ │
│ Tissue Stiff.  │  ████████████░  │ │   - normal zone      │ │
│ [====|====] kPa│                 │ │     shaded green     │ │
│   5.2          │   MARGINAL —    │ │   - patient values   │ │
│                │ INSPECT FURTHER  │ │     as line overlay  │ │
│ Resistive Idx  │                 │ └──────────────────────┘ │
│ [====|====]    │ Confidence: 87% │                          │
│   0.68         │                 │ Feature Contributions    │
│                │ ┌─────────────┐ │ Stiffness  ████████ -22 │
│ Shear Wave Vel │ │Organ-specific│ │ CIT        ██████  -15 │
│ [====|====] m/s│ │risk factors: │ │ RI         █████   -12 │
│   2.1          │ │• CIT at 73%  │ │ Donor Age  ███     -8  │
│                │ │  of limit    │ │ Perfusion  ██████  +14  │
│ Perfusion %    │ │• Stiffness   │ │ SWV        ████    +10  │
│ [====|====]    │ │  borderline  │ │                         │
│   82%          │ └─────────────┘ │                          │
│                │                  │                          │
│ Cold Isch Time │                  │                          │
│ [====|====] hr │                  │                          │
│   14           │                  │                          │
│                │                  │                          │
│ Donor Age      │                  │                          │
│ [====|====] yr │                  │                          │
│   52           │                  │                          │
│                │                  │                          │
│ KDPI / DRI     │                  │                          │
│ [====|====]    │                  │                          │
│   45           │                  │                          │
│                │                  │                          │
│ ┌────────────┐ │                  │                          │
│ │ RUN SCAN ▶ │ │                  │                          │
│ └────────────┘ │                  │                          │
│                │                  │                          │
│ PRESETS:       │                  │                          │
│ [Healthy Kid.] │                  │                          │
│ [Marginal Liv] │                  │                          │
│ [High-Risk Ht] │                  │                          │
│ [The Surprise] │                  │                          │
├────────────────┴──────────────────┴──────────────────────────┤
│  SIMULATED ULTRASOUND WAVEFORM                               │
│  ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿   │
└──────────────────────────────────────────────────────────────┘
```

**Hour 0–1 priorities:** Get Streamlit running, add all input sliders with correct ranges and labels. Use the feature table from the R&D brief as reference (don't wait for BME's spec — the ranges are already in the brief, and you can adjust later).

**Hour 1–2 priorities:** Add the viability score display (big number, colored background), the classification badge, and column layout. Wire sliders to CS #1's placeholder `predict_viability()`.

**Deliverable by Hour 2:** A running app where every slider produces a score output. It won't be pretty yet — that's fine.

### Hour 2–4: Charts & Visual Identity

**Viability gauge (most important visual):**
Use Plotly's `go.Indicator` gauge chart. Color: green (70–100), yellow (40–69), red (0–39). Big, centered, impossible to miss.

**Radar/spider chart:**
Show 6 axes (one per ultrasound parameter). Plot the patient's values as a filled polygon overlaid on a "normal zone" polygon (shaded green). Instantly shows which parameters are out of range. Use Plotly `Scatterpolar`.

**Feature contribution bars:**
Horizontal bar chart. Green bars = features pushing score UP (good perfusion, low CIT). Red bars = features pushing score DOWN (high stiffness, high RI). Sorted by absolute magnitude. Use Plotly or matplotlib.

**Visual identity — make it look clinical, not hacky:**
- Color scheme: dark navy (#1a1a2e) background, white text, accent colors: green (#00d084), amber (#ffb300), red (#ff3d3d) for score tiers
- Clean sans-serif font (Inter, Roboto, or system default)
- Add a header with a subtle medical icon or stethoscope emoji
- If using Streamlit: `st.set_page_config(layout="wide")` and custom CSS via `st.markdown` for the dark theme

### Hour 4–6: Model Integration + Preset Scenarios

**Integration:** CS #1 delivers the real model around Hour 4–5. Swap out the placeholder:

```python
import joblib
model_data = joblib.load("model/model.pkl")

def get_prediction(inputs):
    # Transform inputs to match training format
    features = preprocess(inputs)  # scale, encode organ type, etc.
    score = model_data['reg'].predict(features)[0]
    classification = model_data['clf'].predict(features)[0]
    confidence = max(model_data['clf'].predict_proba(features)[0])
    importances = dict(zip(model_data['feature_names'],
                           model_data['clf'].feature_importances_))
    return score, classification, confidence, importances
```

**Preset scenarios (build as buttons that auto-fill all sliders):**

| Button Label | Story It Tells | Expected Score |
|-------------|---------------|---------------|
| "Healthy Kidney" | Young donor, 6h CIT, normal US across the board | ~90, Accept |
| "Marginal Liver" | Older donor, 14h CIT, elevated stiffness (9 kPa), borderline RI | ~55, Marginal |
| "High-Risk Heart" | Extended criteria, 5h CIT (over limit), poor perfusion, high edema | ~22, Decline |
| "The Surprise" | KDPI = 92 (very high risk by traditional scoring) BUT excellent US features — stiffness 4.2, RI 0.55, perfusion 95% | ~65, Marginal |

**"The Surprise" is your killer demo moment.** It shows that UltraViab can identify transplantable organs that the current system would reject based on donor demographics alone. This directly addresses the discard problem from the keynote. **Make sure the BME narrates this one during the pitch.**

### Hour 6–8: Final Polish

- **Simulated waveform:** A line chart at the bottom showing a generated ultrasound-like signal. Modulate amplitude/frequency based on the input parameters (higher stiffness → different waveform shape). Even a static sine wave with noise looks good. This is purely cosmetic but sells the concept.
- **Responsive layout:** Make sure it looks good on the projection screen (Fontana 1000 will likely have a projector). Test at 1920×1080.
- **Loading animation:** Add a brief spinner or progress bar when "Run Scan" is clicked (even if prediction is instant). Makes it feel like a real device processing data.
- **Help the BME:** Export 2–3 clean screenshots of the dashboard for the pitch deck. Include one screenshot per preset scenario showing different score outputs.

### Hour 6–8 (additional): Help Polish Pitch Deck Visuals

Since there's no second BME to own design, you pick up:
- Making sure the slide deck looks consistent (font, colors, alignment)
- Creating or cleaning up the workflow diagram if the BME's version is rough
- Adding the evaluation plot PNGs from CS #1 into the deck with clean labels
- Formatting the feature table slide so it's readable from the back of the room

### Sunday Morning: Demo Rehearsal & Bulletproofing
- Run the full demo 3+ times with the team
- Test every slider at extreme values — nothing should crash or produce nonsensical output
- Prepare a backup: take screenshots of every preset scenario in case of tech failure during the pitch
- Make sure the app runs on whatever laptop you're presenting from
- If projecting: test font sizes, contrast, and readability at distance

---

## TIMELINE — INTEGRATED VIEW

```
SATURDAY
──────────────────────────────────────────────────────────
Hour    BME                 CS #1               CS #2
──────────────────────────────────────────────────────────
0-1     Feature spec →      Env setup,          UI skeleton,
        share with CS #1    project structure,   all sliders,
        (URGENT)            placeholder API →    basic layout
                            share with CS #2

1-2     Pair with CS #1:    Pair with BME:      Wire sliders to
        define data          code the data       placeholder API,
        distributions       generation script    column layout

2-3     Pair with CS #1:    Pair with BME:      Gauge chart,
        finish synthetic    finish dataset,      radar chart,
        dataset → CSV       export CSV           contribution bars

3-4     Workflow diagram    TRAIN MODEL          Visual polish,
        (for deck + app)    (Random Forest +     dark theme,
                            Gradient Boosting)   clinical styling

4-5     Start pitch deck    Evaluate model,      Continue polish,
        (slides 1-5)        generate plots       preset scenario
                            (ROC, confusion,     buttons
                            feature importance)

5-6     Validate model      Validation loop      MODEL INTEGRATION
        (test edge cases    with BME,            swap placeholder
        with CS #1)         refine thresholds    for real model

6-8     Finish pitch deck,  Edge case handling,  Waveform display,
        add screenshots     input validation,    help polish deck
        + plots to deck,    optional: SHAP       visuals, export
        write demo script                        screenshots
        + speaker notes

8+      Rest / continue     Rest / continue      Rest / continue
──────────────────────────────────────────────────────────

SUNDAY
──────────────────────────────────────────────────────────
8-9     Final deck polish   Bug fixes            Bug fixes,
                                                 test on projector

9-10    Rehearse pitch      Rehearse pitch       Rehearse pitch
        (narrate demo,      (explain ML          (drive demo,
        clinical context)   approach briefly)    handle scenarios)

10-11   SUBMIT DECK         Support              Final demo check
        Export PDF + PPT,   as needed            on presentation
        send to Discord                          laptop

──────────────────────────────────────────────────────────
11 AM — DECKS DUE
12-3 PM — JUDGING
──────────────────────────────────────────────────────────
```

---

## SPEAKING PARTS FOR PITCH

| Section | Speaker | Time | Notes |
|---------|---------|------|-------|
| Intro & Inspiration | BME | 30s | The 2:47 AM scenario. Why this matters. |
| Problem Statement | BME | 45s | Stats, failures, subjective assessment. Clinical authority. |
| What UltraViab Does | BME | 30s | Show workflow diagram. "Scan → Score → Decision." |
| How We Built It | CS #1 | 45s | Tech stack, features, training approach, model choice. |
| Live Demo | CS #2 | 90s | Drive dashboard. 3 scenarios + "The Surprise." BME narrates clinical significance of each result. |
| Results & Validation | CS #1 | 30s | Point to ROC, confusion matrix. "93% accuracy, stiffness is top predictor." |
| Advantages & Impact | BME | 30s | Non-invasive, objective, fast. Reduces discards. Saves lives. |
| Challenges & Future | BME | 30s | Synthetic data caveat. Path to real clinical data. UNOS integration vision. |
| **Total** | | **~5.5 min** | Leaves room for Q&A |

**Note:** The BME does the most speaking (~2.5 min). This is intentional — judges want clinical credibility, and the BME is the one who can speak to WHY this matters and whether the approach is medically sound. The CS students should keep their sections technical and concise.

---

## CRITICAL PATH & RISK MITIGATION

```
BME: Feature Spec (Hour 1) ─────→ CS #1: Can start data generation
BME + CS #1: Dataset (Hour 3) ──→ CS #1: Can train model
CS #1: Placeholder API (Hour 1) → CS #2: Can start building UI
CS #1: Real Model (Hour 5) ─────→ CS #2: Can integrate real predictions
CS #1: Eval Plots (Hour 5) ─────→ BME: Can add to pitch deck
CS #2: Working App (Hour 6) ────→ BME: Can screenshot for deck
```

**Biggest risk: The BME is a single point of failure.**
They own clinical accuracy, the dataset, the pitch deck, and the narrative. If they get stuck on the dataset, the whole project stalls.

**Mitigation strategies:**
1. **CS #1 pairs with BME for Hours 1–3.** Do not let the BME build the dataset alone. CS #1 codes while BME dictates the clinical logic. This is the single most important collaboration window.
2. **CS #2 uses the R&D brief ranges** to start building the UI immediately, without waiting for the BME's final spec. The ranges in the brief are already research-backed — worst case, you adjust slider bounds later.
3. **CS #2 picks up deck visual polish** in Hours 6–8. The BME writes the content; CS #2 makes it look good. This frees the BME to focus on clinical review and speaker notes.
4. **If it's 8 PM and the pitch deck isn't started**, everyone stops and builds the deck together for 1 hour. A great demo with no deck scores zero.

---

## MINIMUM VIABLE DEMO (if you're running behind)

If it's 8 PM Saturday and things aren't coming together, cut to this:

**Keep:**
1. ✅ Streamlit app with sliders + working score (even rule-based)
2. ✅ Color-coded viability gauge (green/yellow/red)
3. ✅ One chart (radar OR feature importance — pick one)
4. ✅ 3 preset scenarios that tell a compelling story
5. ✅ 8-slide pitch deck with workflow diagram

**Cut:**
6. ❌ Animated waveform
7. ❌ SHAP explainability
8. ❌ Multiple organ-specific models (just do kidneys)
9. ❌ Dark theme polish (default Streamlit is fine)
10. ❌ Export/report features

This stripped-down version still scores well on every judging category and can be completed by 2 people if someone drops out.