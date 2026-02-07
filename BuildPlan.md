# UltraViab — MVP Build Plan
## 4-Person Team: 2 CS Majors, 2 BME Students
### BioHack 2026 | ~24 hours | Deadline: Sunday 11 AM

---

## TEAM ROLES AT A GLANCE

| Role | Person | Primary Responsibility | Key Deliverables |
|------|--------|----------------------|------------------|
| **BME #1** | — | Clinical Research Lead & Data Architect | Feature spec, synthetic dataset, clinical validation |
| **BME #2** | — | Pitch Lead & Prototype/Visual Designer | Slide deck, workflow diagrams, UI mockups, 3D print |
| **CS #1** | — | ML Pipeline & Backend | Trained model, API/function, evaluation plots |
| **CS #2** | — | Frontend & Integration | Streamlit/React dashboard, live demo |

---

## BME #1 — "Clinical Research Lead & Data Architect"

This person is the scientific backbone of the project. Everything the CS students build depends on the clinical accuracy of what BME #1 defines. **Speed matters here — CS #1 is blocked until the feature spec and dataset arrive.**

### Hour 0–1: Define the Feature Space

Nail down exactly which measurable parameters the UltraViab system ingests. Use the research brief and Dr. Sellers' keynote as your foundation. You're answering: "If we had a magic ultrasound probe on a donor organ, what numbers would we read off it, and what do they mean?"

**Primary ultrasound-derived features (these are your model inputs):**

| Feature | Unit | Normal Range | Abnormal Range | Source/Rationale |
|---------|------|-------------|----------------|-----------------|
| Tissue stiffness (Young's modulus) | kPa | 3.8–6.0 (liver) | >12 = significant fibrosis, >27 = acute failure | Science Advances 2024, SWE literature |
| Resistive index (RI) | dimensionless | 0.5–0.7 | >0.8 = abnormal arterial resistance | Di Martino et al., multiple Doppler studies |
| Shear wave velocity | m/s | 1.8–2.2 (kidney cortex) | >2.6 = elevated stiffness, worse outcomes | PMC 2023, OR=17.1 for adverse outcomes |
| Perfusion uniformity score | 0–100% | >85% = uniform | <60% = significant perfusion defects | CEUS pancreas study, conceptual |
| Echogenicity grade | 1–5 scale | 1–2 = homogeneous | 4–5 = heterogeneous/concerning | B-mode assessment standards |
| Edema index | 0–10 scale | 0–3 | >6 = significant tissue swelling | Derived from parenchymal assessment |

**Donor/clinical metadata features (context the model also uses):**

| Feature | Unit | Range | Notes |
|---------|------|-------|-------|
| Cold ischemia time (CIT) | hours | 0–40+ | Kidney: 24–36h tolerance; Liver: 12–18h; Heart: ~4h |
| Organ type | categorical | kidney, liver, heart, lung | Different thresholds per organ |
| Donor age | years | 0–80 | Older donors = higher baseline risk |
| KDPI (kidneys) / DRI (livers) | percentile/score | 0–100 | Donor quality index |
| Donor cause of death | categorical | trauma, CVA, anoxia, other | Affects organ quality |
| Donor BMI | kg/m² | 15–50 | Higher BMI = more steatosis in livers |
| Warm ischemia time | minutes | 0–60 | Especially important for DCD organs |

**Deliverable:** A clean Google Sheet or markdown table with every feature, its unit, range, clinical meaning, and source. Share with CS #1 by end of Hour 1.

### Hour 1–3: Build the Synthetic Training Dataset

This is the most critical task. CS #1 cannot train the model without this. You're generating ~500–1000 rows of simulated organ assessments. Each row represents one organ with all features filled in and a labeled outcome.

**Outcome labels (what the model predicts):**
- **Accept (viable)** — Score 70–100. Organ shows healthy parameters, expected good graft function
- **Marginal (inspect further)** — Score 40–69. Some concerning features but potentially transplantable
- **Decline (non-viable)** — Score 0–39. Multiple red flags, high risk of graft failure

**How to generate realistic data:**
1. Define the joint distributions — viable organs cluster around normal ranges; non-viable organs have correlated abnormalities (high stiffness AND high RI AND long CIT tend to go together)
2. Add realistic noise — not every bad organ has all bad numbers. Some marginal organs have one alarming feature but others look fine
3. Organ-type-specific logic — a liver at 20h CIT is concerning; a kidney at 20h is within tolerance
4. Use published correlations: each additional hour of CIT increases graft failure risk; KDPI >85% is high-risk regardless of other factors

**Practical approach:** Write this in Python with numpy/pandas, or even manually in a spreadsheet with formulas. CS #1 can help you script the generation if needed.

**Deliverable:** A CSV file (`training_data.csv`) with 500–1000 rows, all features as columns, plus a `viability_label` column (accept/marginal/decline) and a `viability_score` column (0–100). Delivered to CS #1 by Hour 3.

### Hour 3–5: Clinical Validation Loop

Once CS #1 has a trained model (~Hour 4), start testing it:
- Feed in edge cases: "What does the model say about a 65-year-old donor kidney with 30h CIT but perfect ultrasound numbers?" — should probably be Marginal, not Decline
- Feed in obvious cases: "Young donor, 4h CIT, all normal US parameters" — must be Accept
- Feed in trap cases: "Great ultrasound features but KDPI = 95%" — should the US data override the donor risk index? This is where your clinical judgment shapes the model
- Document any cases where the model gets it wrong and feed corrections back to CS #1

**Deliverable:** A validation report (even just notes) listing 10–15 test cases with expected vs. actual model output, plus any threshold adjustments needed.

### Hour 5–8: Support Pitch Deck Content

Work with BME #2 to fill in the clinical slides:
- The specific problem (20–30% discard rate, 100K+ waitlist, subjective assessment)
- How current viability assessment works (and where it fails)
- What published science supports this approach (cite the key papers)
- A realistic use case scenario: "It's 2:47 AM, a kidney arrives from Pittsburgh..."

### Hour 8–11 (Sunday morning): Final Clinical Review
- Review the dashboard outputs with fresh eyes
- Confirm the feature importance ranking makes clinical sense
- Help BME #2 rehearse the clinical narrative for the pitch

---

## BME #2 — "Pitch Lead & Prototype/Visual Designer"

This person owns the **story** and the **physical/visual artifacts**. In a hackathon, presentation quality often separates winners from runners-up. You're making sure judges understand why this matters and that the demo looks polished and professional.

### Hour 0–2: Clinical Workflow Diagram & UI Wireframe

**Workflow diagram:** Create a clear visual showing where UltraViab fits in the transplant pipeline. Reference the Health Universe challenge slides (Step 1: Donor ID → Step 2: Authorization → Step 3: Match Run → Step 4: Offer Cascade → **Step 4.5: UltraViab Scan** → Step 5: Recovery & Transport → Step 6: Transplant). Show that the scan happens at the donor hospital before/during organ recovery, and the viability score is transmitted digitally to accepting centers.

**UI wireframe:** Sketch (paper or Figma/draw.io) the dashboard layout for CS #2:
- Left panel: Input form (organ type dropdown, sliders for each US parameter, donor metadata fields)
- Center: Large viability gauge (0–100, color gradient red→yellow→green), classification badge (Accept/Marginal/Decline)
- Right: Radar chart showing each parameter's contribution, with "normal zone" shaded
- Bottom: Simulated ultrasound waveform display (for visual impact)
- Top bar: Organ type selector, patient ID field, timestamp

**Deliverable:** A workflow diagram image (Canva, PowerPoint, draw.io, or hand-drawn and photographed) and a UI wireframe sketch. Share wireframe with CS #2 by Hour 2.

### Hour 2–5: Pitch Deck — First Draft

Build the slide deck structure (PowerPoint or Google Slides). This must be submitted by 11 AM Sunday. Follow the judging rubric exactly:

| Slide | Content | Time |
|-------|---------|------|
| 1 | Title slide: "UltraViab: Non-Invasive Organ Viability Scoring" | 10 sec |
| 2 | **Inspiration** — Why you chose this problem. Personal connection if possible. The 2:47 AM scenario. | 30 sec |
| 3 | **Problem Statement** — 20–30% discard rate. 100K+ waitlist. Subjective assessment. Biopsy increases discard. Quote Dr. Sellers' keynote points. | 45 sec |
| 4 | **What It Does** — High-level: portable US probe + ML model = objective viability score in minutes. Show the workflow diagram. | 45 sec |
| 5 | **How We Built It** — Tech stack: Python/scikit-learn for ML, Streamlit/React for dashboard, synthetic data from published clinical thresholds. Show the feature table. | 45 sec |
| 6 | **Live Demo** — CS #2 drives. Show a kidney case: plug in numbers, get score. Then show a liver case. Then show an edge case. | 90 sec |
| 7 | **Advantages** — Non-invasive (unlike biopsy). Objective (unlike visual inspection). Fast (minutes, not hours). Portable. Works with existing US hardware. | 30 sec |
| 8 | **Technical Details** — Model performance: ROC curve, confusion matrix, feature importance. Show the validation cases BME #1 tested. | 45 sec |
| 9 | **Challenges & What We Learned** — Synthetic data limitations, threshold calibration, organ-specific differences. What we'd do with real data. | 30 sec |
| 10 | **Future Vision** — Integration with machine perfusion devices, UNOS/OPTN system, prospective clinical validation path. Health Universe deployment. | 30 sec |
| 11 | Thank you / Q&A | — |

**Deliverable:** Slide deck first draft by Hour 5. Does not need to be perfect — content and structure matter more at this stage. Polish happens later.

### Hour 2–5 (parallel): Optional 3D Print or Physical Prototype

If you want a hardware component (judges appreciate tangible artifacts), consider:
- **Option A:** 3D print a simplified "probe housing" — a rectangular case roughly the size of a portable US probe with a flat scanning surface. Purely cosmetic but powerful for the demo. **Remember: 5 PM deadline to start prints.**
- **Option B:** 3D print a stylized organ transport container insert with a recess labeled "UltraViab sensor placement." Shows where the probe would sit during transport.
- **Option C:** Skip the print, focus on a really polished digital demo instead. This is totally fine.

If printing, get the STL file designed and submitted by 3–4 PM Saturday at the latest.

### Hour 5–8: Polish Deck + Prepare Demo Script

- Add screenshots from the working dashboard (CS #2 will have a functional UI by now)
- Add the ML evaluation plots from CS #1
- Write speaker notes for each slide
- Create a demo script: exactly which inputs to type, in what order, what to point out
- Practice the pitch timing — you're aiming for 5–7 minutes total

### Hour 8–11 (Sunday morning): Final Polish & Rehearsal
- Incorporate any last-minute dashboard improvements into slides
- Full team rehearsal: 2–3 runthroughs
- Assign speaking parts: BME #2 does Intro/Problem/Vision, BME #1 does Clinical Details/Advantages, CS #1 does Technical Architecture, CS #2 does Live Demo
- Export final deck as PDF and PowerPoint, submit to Discord channel before 11 AM

---

## CS #1 — "ML Pipeline & Backend"

You own the intelligence behind UltraViab. Your job is to turn clinical data into a reliable prediction.

### Hour 0–2: Environment Setup & Pipeline Skeleton

While waiting for BME #1's feature spec and dataset:

```
# Set up project structure
ultraviab/
├── data/
│   └── training_data.csv          # From BME #1
├── model/
│   ├── train.py                   # Training script
│   ├── predict.py                 # Prediction function
│   ├── evaluate.py                # Evaluation metrics & plots
│   └── model.pkl                  # Saved model
├── app/
│   └── streamlit_app.py           # Or React app (CS #2 owns this)
├── utils/
│   └── generate_synthetic_data.py # Help BME #1 if needed
└── outputs/
    ├── roc_curve.png
    ├── confusion_matrix.png
    └── feature_importance.png
```

- Install dependencies: `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `joblib`
- Write the `predict.py` interface: `def predict_viability(organ_type, stiffness, ri, swv, perfusion, echogenicity, edema, cit, donor_age, kdpi, ...) -> dict` returning `{"score": 0-100, "classification": "accept/marginal/decline", "confidence": 0-1, "feature_contributions": {...}}`
- Write placeholder logic (rule-based) so CS #2 can start integrating immediately
- Help BME #1 script the synthetic data generation if they want Python help

### Hour 2–4: Train the Model

Once `training_data.csv` arrives:

**Approach — start simple, add complexity only if time permits:**

1. **Random Forest Classifier** (primary) — handles nonlinear interactions, gives feature importances out of the box, robust to noisy features. Train on the 3-class problem (accept/marginal/decline).

2. **Gradient Boosted Regressor** (secondary) — for the continuous viability score (0–100). This gives you the numeric score while the RF gives the classification.

3. **Cross-validation:** 5-fold CV on the synthetic data. Report accuracy, precision, recall, F1 per class.

4. **Feature importance:** Extract and plot. This is one of your most important demo artifacts — it shows judges what the model learned (e.g., "tissue stiffness is the strongest predictor, followed by cold ischemia time, then resistive index").

**Key modeling decisions:**
- Normalize/scale features (StandardScaler) since they're on very different scales (kPa vs. hours vs. 0–1)
- Handle organ type as a categorical variable (one-hot encode or train separate models per organ)
- Consider training organ-specific models if the thresholds are very different (they are — heart CIT tolerance is 4h vs. kidney 36h)

**Deliverable by Hour 4:** A trained model saved to `model.pkl`, a `predict_viability()` function that CS #2 can call, and initial evaluation plots.

### Hour 4–6: Evaluation & Clinical Validation Support

Generate the artifacts that go in the pitch deck:

- **ROC Curve:** Plot per-class ROC with AUC values. Even on synthetic data, this shows the model architecture works.
- **Confusion Matrix:** Heatmap showing predictions vs. actual labels. Ideally very few "Accept" organs classified as "Decline" (false negatives are the worst — you'd discard a viable organ).
- **Feature Importance Bar Chart:** Horizontal bar chart, sorted. Color code by feature category (ultrasound-derived vs. donor metadata). Story to tell: "Our model shows ultrasound tissue stiffness is 2.3x more predictive than donor age alone — this is why non-invasive acoustic assessment adds value over existing donor scoring."
- **Sensitivity Analysis:** How does the viability score change when you sweep one feature while holding others constant? E.g., plot score vs. CIT for an otherwise-healthy kidney. Shows the "degradation curve."

Work with BME #1 on the validation loop (test cases, edge cases, clinical plausibility check).

**Deliverable:** PNG/SVG exports of all plots, ready for the pitch deck.

### Hour 6–8: Integration & Edge Cases

- Make sure `predict_viability()` handles all organ types correctly
- Add input validation (e.g., CIT can't be negative, RI must be 0–1)
- Stress-test with weird inputs CS #2 might pass from the UI
- If time: add a SHAP or LIME explainability layer (very impressive for judges, but not essential)
- If time: compare performance of Random Forest vs. Gradient Boosted vs. simple Logistic Regression and show that RF wins — demonstrates you explored multiple approaches

### Hour 8–11 (Sunday morning): Bug Fixes & Demo Support
- Be on standby for any backend issues during demo rehearsal
- Export final model performance numbers for the pitch deck
- Help CS #2 with any last-minute integration issues

---

## CS #2 — "Frontend & Integration Lead"

You own the demo. In a hackathon, a beautiful, working demo is worth more than a perfect model. Judges need to see it, touch it, and understand it in 90 seconds.

### Hour 0–2: Dashboard Skeleton with Placeholder Data

Don't wait for the model. Start building the UI now with hardcoded values.

**Recommended stack:** Streamlit (fastest to build, built-in widgets, good enough for a hackathon) OR React with Tailwind (prettier but slower to build). For a 24-hour hack, Streamlit is the safer bet unless you're very fast with React.

**Layout (from BME #2's wireframe):**

```
┌─────────────────────────────────────────────────────────┐
│  🔬 UltraViab — Organ Viability Assessment System       │
│  [Kidney ▼]  Patient ID: [____]  Scan Time: 02:47 AM   │
├───────────────┬─────────────────┬───────────────────────┤
│ INPUT PANEL   │  VIABILITY      │  PARAMETER ANALYSIS   │
│               │  SCORE          │                       │
│ Organ Type    │                 │  [Radar/Spider Chart] │
│ [dropdown]    │    ┌───┐        │  showing each param   │
│               │    │78 │        │  vs. normal range     │
│ Tissue Stiff  │    └───┘        │                       │
│ [===|===] kPa │  ██████████░░   │  Feature Contribution │
│               │  MARGINAL -     │  [horizontal bars]    │
│ Resistive Idx │  INSPECT FURTHER│                       │
│ [===|===]     │                 │                       │
│               │  Confidence: 87%│                       │
│ Shear Wave V  │                 │                       │
│ [===|===] m/s │                 │                       │
│               │                 │                       │
│ Perfusion     │                 │                       │
│ [===|===] %   │                 │                       │
│               │                 │                       │
│ CIT (hours)   │                 │                       │
│ [===|===]     │                 │                       │
│               │                 │                       │
│ Donor Age     │                 │                       │
│ [===|===]     │                 │                       │
│               │                 │                       │
│ KDPI          │                 │                       │
│ [===|===]     │                 │                       │
│               │                 │                       │
│ [RUN SCAN]    │                 │                       │
├───────────────┴─────────────────┴───────────────────────┤
│  SIMULATED ULTRASOUND WAVEFORM                          │
│  ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿   │
└─────────────────────────────────────────────────────────┘
```

**Key UI elements to build first:**
1. Organ type selector (dropdown: Kidney, Liver, Heart, Lung)
2. Sliders for each ultrasound parameter with labeled ranges (green/yellow/red zones)
3. Large viability score display (number + color + classification text)
4. "Run Assessment" button that triggers the prediction

**Placeholder logic until model is ready:**
```python
# Simple rule-based placeholder
score = 100 - (stiffness * 2) - (ri * 30) - (cit * 1.5) - (donor_age * 0.3)
score = max(0, min(100, score))
```

**Deliverable by Hour 2:** A running Streamlit app with all input widgets and a placeholder score output.

### Hour 2–4: Visual Polish & Charts

- **Viability gauge:** Use Plotly's gauge chart or a custom radial progress bar. Color: green (70–100), yellow (40–69), red (0–39). This is the visual centerpiece.
- **Radar/spider chart:** Show each parameter as an axis, with the "normal zone" as a shaded polygon and the patient's values as a line. Instantly shows which parameters are out of range.
- **Feature contribution bars:** Horizontal bar chart showing how much each input pushed the score up or down. Green bars = positive contributors, red bars = risk factors.
- **Simulated waveform:** A simple animated line chart (sine wave + noise, modulated by the input parameters). Purely cosmetic but sells the "ultrasound" concept. Even a static waveform image works.

### Hour 4–6: Model Integration

CS #1 delivers the trained model. Swap out placeholder logic:

```python
import joblib
model = joblib.load("model/model.pkl")

def get_prediction(features):
    # features = dict of input values
    score = model.predict_proba(features)  # or regression score
    classification = model.predict(features)
    return score, classification
```

- Wire up every slider to pass through the model
- Make the UI update in real-time as sliders move (Streamlit handles this natively)
- Add the feature importance data from CS #1's model to the contribution bar chart

### Hour 6–8: Demo Scenarios & Final Polish

Build in **preset scenarios** that load pre-filled inputs with one click:

| Scenario Button | Description | Expected Output |
|----------------|-------------|-----------------|
| "Healthy Kidney" | Young donor, 6h CIT, normal US | Score ~90, Accept |
| "Marginal Liver" | Older donor, 14h CIT, elevated stiffness | Score ~55, Marginal |
| "High-Risk Heart" | Extended criteria, 5h CIT, poor perfusion | Score ~25, Decline |
| "The Surprise" | High KDPI but excellent US features | Score ~65, Marginal — shows US can rescue organs the KDPI alone would reject |

These preset scenarios are your demo script. BME #2 and you should agree on exactly which scenarios to show during the pitch.

**Additional polish:**
- Add a subtle animation when the score updates
- Dark theme with clinical feel (dark navy/charcoal background, white text, accent colors for score)
- "Export Report" button (generates a text summary — doesn't need to be a real PDF)
- Add the team name, BioHack logo, and Health Universe logo somewhere in the header
- Mobile-responsive if using React (judges may view on phones)

### Hour 8–11 (Sunday morning): Demo Rehearsal & Bug Fixes
- Run through the full demo 3+ times with the team
- Test every slider at extreme values (make sure nothing crashes)
- Have a backup plan: screenshots of the working app in case of technical difficulties during the pitch
- Deploy locally — make sure it runs on whatever laptop you're presenting from

---

## TIMELINE — INTEGRATED VIEW

```
SATURDAY
────────────────────────────────────────────────────────────────
Hour    BME #1              BME #2              CS #1               CS #2
────────────────────────────────────────────────────────────────
0-1     Feature spec &      Workflow diagram    Env setup,          UI skeleton,
        threshold research  + UI wireframe      project structure   placeholder app

1-2     Feature spec →      UI wireframe →      Pipeline skeleton,  Build sliders,
        share with CS #1    share with CS #2    placeholder API     input panel

2-3     Build synthetic     Start pitch deck    Help BME #1 with    Add gauge chart,
        dataset (Python     (slides 1-5)        data generation     radar chart
        or spreadsheet)                         if needed

3-4     Dataset → CS #1     Pitch deck cont.    TRAIN MODEL         Visual polish,
        (CSV handoff)       (slides 6-10)       (Random Forest)     waveform display

4-5     Start validation    Optional: 3D print  Evaluate model,     Continue charts,
        test cases          design/submit       generate plots      preset scenarios

5-6     Validation loop     Add screenshots     ROC, confusion      MODEL INTEGRATION
        with CS #1          to deck from app    matrix, feature     (swap placeholder)
                                                importance

6-8     Review model        Polish deck,        Edge cases,         Demo scenarios,
        outputs, iterate    write speaker       stress testing,     final UI polish,
        thresholds          notes, demo script  optional SHAP       dark theme

8-??    Rest / continue     Rest / continue     Rest / continue     Rest / continue
────────────────────────────────────────────────────────────────

SUNDAY
────────────────────────────────────────────────────────────────
8-9     Final clinical      Final deck polish   Bug fixes           Bug fixes
        review                                  

9-10    Practice pitch      Practice pitch      Practice pitch      Practice pitch
        (clinical parts)    (lead presenter)    (technical parts)   (run live demo)

10-11   SUBMIT DECK         SUBMIT DECK         Support             Test demo on
        Review & send       Export PDF + PPT    as needed           presentation
                                                                    laptop
────────────────────────────────────────────────────────────────
11 AM — DECKS DUE
12-3 PM — JUDGING
────────────────────────────────────────────────────────────────
```

---

## SPEAKING PARTS FOR PITCH (suggested)

| Section | Speaker | Time | Notes |
|---------|---------|------|-------|
| Intro & Inspiration | BME #2 | 30s | Set the scene. The 2:47 AM call. |
| Problem Statement | BME #1 | 45s | Clinical authority. Stats, failures, what's broken. |
| What UltraViab Does | BME #2 | 45s | Show workflow diagram. High-level concept. |
| Technical Deep Dive | CS #1 | 45s | ML approach, features, model performance plots. |
| Live Demo | CS #2 | 90s | Drive the dashboard. 3 scenarios. |
| Advantages & Impact | BME #1 | 30s | Non-invasive, objective, fast. Lives saved. |
| Challenges & Future | BME #2 | 30s | Honest about synthetic data. Path to clinical validation. |
| **Total** | | **~5.5 min** | Leaves room for Q&A |

---

## CRITICAL PATH & DEPENDENCIES

```
BME #1: Feature Spec (Hour 1) ──→ CS #1: Can start pipeline
BME #1: Synthetic Data (Hour 3) ──→ CS #1: Can train model
BME #2: UI Wireframe (Hour 2) ──→ CS #2: Knows what to build
CS #1: Trained Model (Hour 4) ──→ CS #2: Can integrate real predictions
CS #1: Eval Plots (Hour 5) ──→ BME #2: Can add to pitch deck
CS #2: Working App (Hour 6) ──→ BME #2: Can screenshot for deck
```

**Biggest bottleneck:** BME #1's synthetic dataset. If this is late, everything downstream shifts. Mitigation: CS #1 should help BME #1 script the data generation in Python if BME #1 isn't comfortable with it. Don't let this person struggle alone with a spreadsheet — pair up.

---

## MINIMUM VIABLE DEMO (if you're running behind)

If it's 8 PM Saturday and things aren't coming together, cut scope to this:

1. ✅ Streamlit app with sliders and a working score (even rule-based, not ML)
2. ✅ Color-coded viability gauge
3. ✅ One chart (radar OR feature importance, not both)
4. ✅ 3 preset scenarios that tell a compelling story
5. ✅ 8-slide pitch deck
6. ❌ Skip: animated waveform, 3D print, SHAP, multiple organ models, export feature

This stripped-down version still scores well on every judging criterion and can be built by 2 people if needed.