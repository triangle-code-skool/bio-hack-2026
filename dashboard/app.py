import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
import requests

# --- Page Config ---
st.set_page_config(
    page_title="UltraViab | Organ Viability",
    page_icon="\U0001f52c",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown(
    """
<style>
/* ---- Global ---- */
.stApp {
    background: linear-gradient(170deg, #0a0e17 0%, #101828 100%);
    color: #e0e6ed;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f1f5f9;
}

/* Headings */
h1, h2, h3, h4 { color: #f1f5f9; }

/* Primary action button */
.stButton>button {
    width: 100%;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 700;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
/* Run Scan button — green accent */
div[data-testid="stVerticalBlock"] > div:first-child .stButton>button {
    background: linear-gradient(135deg, #00d084, #00b371);
    color: #fff;
    font-size: 1rem;
}
div[data-testid="stVerticalBlock"] > div:first-child .stButton>button:hover {
    background: linear-gradient(135deg, #00e693, #00c07e);
    box-shadow: 0 0 18px rgba(0,208,132,0.35);
}

/* Preset buttons — subtle dark */
.stButton>button {
    background: #1e293b;
    color: #94a3b8;
    font-size: 0.82rem;
}
.stButton>button:hover {
    background: #334155;
    color: #e2e8f0;
    box-shadow: 0 0 12px rgba(148,163,184,0.15);
}

/* Metric card */
.metric-card {
    background: #1e293b;
    padding: 1.5rem 2rem;
    border-radius: 0.75rem;
    border: 1px solid #334155;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}

/* Score value */
.score-value {
    font-size: 5.5rem;
    font-weight: 800;
    line-height: 1;
    margin: 0.25rem 0;
    font-variant-numeric: tabular-nums;
}

/* Status badge */
.status-badge {
    display: inline-block;
    padding: 0.25rem 0.85rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* Section divider */
.section-divider {
    border: none;
    border-top: 1px solid #1e293b;
    margin: 1.5rem 0;
}

/* Info box styling */
div[data-testid="stAlert"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 0.5rem;
    color: #94a3b8;
}

/* Slider track */
.stSlider > div > div > div {
    color: #94a3b8 !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Smooth fade-in for results */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeSlideIn 0.45s ease-out;
}
</style>
""",
    unsafe_allow_html=True,
)


# ──────────────────────────────────────
# Sidebar
# ──────────────────────────────────────
st.sidebar.markdown("## \U0001f52c UltraViab")
st.sidebar.caption("Non-Invasive Organ Viability Assessment")
st.sidebar.markdown("---")

st.sidebar.markdown("### Organ Metadata")
organ_type = st.sidebar.selectbox(
    "Organ Type", ["Kidney", "Liver", "Heart", "Lung"], key="organ_type"
)
donor_age = st.sidebar.slider(
    "Donor Age", 0, 100, 45, key="donor_age", help="Age of the donor in years"
)
cit_hours = st.sidebar.slider(
    "Cold Ischemia Time (hrs)", 0.0, 40.0, 12.0, 0.5, key="cit_hours"
)
kdpi = st.sidebar.slider(
    "KDPI / DRI (%)", 0, 100, 40, key="kdpi", help="Kidney Donor Profile Index"
)
cause_death = st.sidebar.selectbox(
    "Cause of Death", ["Trauma", "Anoxia", "CVA", "Other"], key="cause_death"
)

st.sidebar.markdown("### Ultrasound Parameters")
stiffness = st.sidebar.slider(
    "Tissue Stiffness (kPa)",
    0.0,
    30.0,
    5.2,
    0.1,
    key="stiffness",
    help="Normal: 3.8\u20136.0 kPa (Liver)",
)
ri = st.sidebar.slider(
    "Resistive Index (RI)",
    0.0,
    1.2,
    0.65,
    0.01,
    key="ri",
    help="Normal: 0.5\u20130.7",
)
swv = st.sidebar.slider(
    "Shear Wave Velocity (m/s)", 0.0, 5.0, 2.1, 0.1, key="swv"
)
perfusion = st.sidebar.slider(
    "Perfusion Uniformity (%)",
    0,
    100,
    85,
    key="perfusion",
    help=">85% is ideal",
)
echogenicity = st.sidebar.slider(
    "Echogenicity Grade",
    1,
    5,
    2,
    key="echogenicity",
    help="1 = Homogeneous, 5 = Heterogeneous",
)
edema = st.sidebar.slider(
    "Edema Index", 0, 10, 2, key="edema", help="0 = None, 10 = Severe"
)
warm_ischemia = st.sidebar.slider(
    "Warm Ischemia Time (min)", 0, 120, 15, key="warm_ischemia"
)


# ──────────────────────────────────────
# Presets
# ──────────────────────────────────────
PRESETS = {
    "Healthy Kidney": dict(
        organ_type="Kidney",
        donor_age=25,
        cit_hours=6.0,
        stiffness=4.5,
        ri=0.6,
        swv=1.9,
        perfusion=95,
        kdpi=20,
        echogenicity=1,
        edema=1,
        warm_ischemia=10,
        cause_death="Trauma",
    ),
    "Marginal Liver": dict(
        organ_type="Liver",
        donor_age=55,
        cit_hours=14.0,
        stiffness=9.0,
        ri=0.75,
        swv=2.5,
        perfusion=75,
        kdpi=65,
        echogenicity=3,
        edema=4,
        warm_ischemia=25,
        cause_death="CVA",
    ),
    "High-Risk Heart": dict(
        organ_type="Heart",
        donor_age=60,
        cit_hours=5.0,
        stiffness=12.0,
        ri=0.9,
        swv=3.2,
        perfusion=50,
        kdpi=80,
        echogenicity=4,
        edema=8,
        warm_ischemia=40,
        cause_death="Anoxia",
    ),
    "The Surprise": dict(
        organ_type="Kidney",
        donor_age=62,
        cit_hours=18.0,
        stiffness=4.2,
        ri=0.55,
        swv=1.8,
        perfusion=95,
        kdpi=92,
        echogenicity=2,
        edema=2,
        warm_ischemia=18,
        cause_death="CVA",
    ),
}


def load_preset(name: str) -> None:
    for k, v in PRESETS[name].items():
        st.session_state[k] = v
    st.toast(f"Preset loaded: {name}")


# ──────────────────────────────────────
# Header
# ──────────────────────────────────────
st.markdown(
    """
<div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.25rem;">
    <span style="font-size:2rem;">\U0001f9ec</span>
    <span style="font-size:1.8rem; font-weight:800; color:#f1f5f9;">UltraViab</span>
    <span style="font-size:0.9rem; color:#64748b; margin-left:0.25rem; padding-top:0.35rem;">
        Non-Invasive Organ Viability Assessment
    </span>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='color:#64748b; margin:0 0 1rem 0; font-size:0.85rem;'>"
    "Scan ID: <code style='color:#00d084;'>UV-2026-0207</code> &nbsp;|&nbsp; "
    "Status: <strong style='color:#00d084;'>Ready</strong></p>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ──────────────────────────────────────
# Main layout
# ──────────────────────────────────────
col_action, col_results = st.columns([1, 3])

with col_action:
    run_scan = st.button("\u25b6  RUN SCAN", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b; font-size:0.78rem; text-transform:uppercase; "
        "letter-spacing:0.08em; font-weight:600; margin-bottom:0.5rem;'>Quick Presets</p>",
        unsafe_allow_html=True,
    )

    for label in PRESETS:
        if st.button(label, use_container_width=True):
            load_preset(label)
            st.rerun()

    # Organ quick-stats panel
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748b; font-size:0.78rem; text-transform:uppercase; "
        "letter-spacing:0.08em; font-weight:600; margin-bottom:0.5rem;'>Current Inputs</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class='metric-card' style='font-size:0.82rem; line-height:1.85; padding:1rem;'>
    <strong style='color:#00d084;'>{organ_type}</strong><br>
    Donor Age: <strong>{donor_age}</strong> yrs<br>
    CIT: <strong>{cit_hours}</strong> hrs<br>
    Stiffness: <strong>{stiffness}</strong> kPa<br>
    RI: <strong>{ri}</strong><br>
    Perfusion: <strong>{perfusion}%</strong><br>
    KDPI: <strong>{kdpi}%</strong>
</div>""",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────
# Scan logic & results
# ──────────────────────────────────────
if run_scan:
    with st.spinner("Processing ultrasound data\u2026"):
        time.sleep(1.0)

        api_url = "http://localhost:8000/predict"
        payload = {
            "organ_type": organ_type,
            "tissue_stiffness_kpa": stiffness,
            "resistive_index": ri,
            "shear_wave_velocity_ms": swv,
            "perfusion_uniformity_pct": perfusion,
            "echogenicity_grade": echogenicity,
            "edema_index": edema,
            "cold_ischemia_hours": cit_hours,
            "donor_age": donor_age,
            "kdpi_percentile": kdpi,
            "cause_of_death": cause_death,
            "warm_ischemia_minutes": warm_ischemia,
        }

        confidence = None
        try:
            response = requests.post(api_url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                score = data["viability_score"]
                status = data["classification"]
                confidence = data.get("confidence")
                risk_factors = data.get("risk_factors", [])
                msg = (
                    f"Notable risks: {', '.join(risk_factors)}."
                    if risk_factors
                    else "No significant risk factors detected."
                )
            else:
                st.error(f"API returned status {response.status_code}")
                score, status, msg = 50, "API ERROR", "Could not reach backend."
        except Exception:
            st.warning("Backend offline \u2014 using simulation mode.")
            # Fallback scoring
            score = 100.0
            score -= max(0, (stiffness - 5.0) * 3)
            score -= max(0, (ri - 0.7) * 40)
            score -= max(0, (cit_hours - 12) * 1.5)
            score -= max(0, (donor_age - 50) * 0.3)
            score -= (100 - perfusion) * 0.2
            score -= max(0, (echogenicity - 2) * 4)
            score -= max(0, (edema - 3) * 3)
            score = max(0, min(100, score))

            if score >= 70:
                status, msg = "ACCEPT", "Organ shows excellent viability. (Simulated)"
            elif score >= 40:
                status, msg = "MARGINAL", "Borderline parameters detected. (Simulated)"
            else:
                status, msg = "DECLINE", "High-risk features detected. (Simulated)"

        color_map = {
            "Accept": "#00d084",
            "ACCEPT": "#00d084",
            "Marginal": "#f59e0b",
            "MARGINAL": "#f59e0b",
            "Decline": "#ef4444",
            "DECLINE": "#ef4444",
        }
        color = color_map.get(status, "#64748b")
        badge_bg = {
            "Accept": "rgba(0,208,132,0.15)",
            "ACCEPT": "rgba(0,208,132,0.15)",
            "Marginal": "rgba(245,158,11,0.15)",
            "MARGINAL": "rgba(245,158,11,0.15)",
            "Decline": "rgba(239,68,68,0.15)",
            "DECLINE": "rgba(239,68,68,0.15)",
        }.get(status, "rgba(100,116,139,0.15)")

        conf_display = (
            f"{confidence:.0%}" if confidence is not None else "N/A"
        )

    # ---- Display results ----
    with col_results:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)

        # Score card
        st.markdown(
            f"""
<div class='metric-card' style='border-left: 6px solid {color}; margin-bottom:1.25rem;'>
    <p style='margin:0; color:#64748b; font-size:0.75rem; text-transform:uppercase;
       letter-spacing:0.1em; font-weight:600;'>Viability Score</p>
    <div class='score-value' style='color:{color};'>{int(score)}</div>
    <span class='status-badge' style='background:{badge_bg}; color:{color};'>{status}</span>
    <span style='margin-left:0.75rem; color:#64748b; font-size:0.82rem;'>
        Confidence: {conf_display}
    </span>
    <p style='margin-top:0.75rem; color:#94a3b8; font-size:0.88rem;'>{msg}</p>
</div>""",
            unsafe_allow_html=True,
        )

        # Charts
        chart_left, chart_right = st.columns(2)

        # ---- Radar chart ----
        with chart_left:
            st.markdown(
                "<p style='color:#94a3b8; font-size:0.78rem; text-transform:uppercase; "
                "letter-spacing:0.08em; font-weight:600;'>Parameter Analysis</p>",
                unsafe_allow_html=True,
            )

            categories = ["Stiffness", "RI", "CIT", "Age", "Perfusion", "SWV"]
            values = [
                min(1, stiffness / 15.0),
                min(1, ri / 1.0),
                min(1, cit_hours / 40.0),
                min(1, donor_age / 100.0),
                min(1, (100 - perfusion) / 100.0),
                min(1, swv / 4.0),
            ]
            normal_limits = [0.4, 0.7, 0.3, 0.5, 0.15, 0.55]

            fig_radar = go.Figure()

            # Normal zone (filled green area)
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=normal_limits,
                    theta=categories,
                    fill="toself",
                    name="Normal Zone",
                    fillcolor="rgba(0,208,132,0.08)",
                    line=dict(color="rgba(0,208,132,0.4)", dash="dash", width=1),
                )
            )

            # Organ values
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill="toself",
                    name="Current Organ",
                    fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12)",
                    line=dict(color=color, width=2),
                )
            )

            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        showticklabels=False,
                        gridcolor="rgba(148,163,184,0.1)",
                    ),
                    angularaxis=dict(
                        gridcolor="rgba(148,163,184,0.1)",
                        linecolor="rgba(148,163,184,0.1)",
                    ),
                ),
                showlegend=True,
                legend=dict(
                    font=dict(size=10, color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                margin=dict(l=40, r=40, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8", size=11),
                height=320,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # ---- Risk factor bar chart ----
        with chart_right:
            st.markdown(
                "<p style='color:#94a3b8; font-size:0.78rem; text-transform:uppercase; "
                "letter-spacing:0.08em; font-weight:600;'>Risk Factor Contributions</p>",
                unsafe_allow_html=True,
            )

            contribs = {
                "Stiffness": -max(0, (stiffness - 5.0) * 3),
                "Resistive Index": -max(0, (ri - 0.7) * 40),
                "Cold Ischemia": -max(0, (cit_hours - 12) * 1.5),
                "Donor Age": -max(0, (donor_age - 50) * 0.3),
                "Perfusion": 10 if perfusion > 80 else -5,
                "Echogenicity": -max(0, (echogenicity - 2) * 4),
                "Edema": -max(0, (edema - 3) * 3),
            }

            contrib_df = pd.DataFrame(
                list(contribs.items()), columns=["Feature", "Impact"]
            )
            contrib_df = contrib_df.sort_values("Impact", ascending=True)

            bar_colors = [
                "#ef4444" if v < 0 else "#00d084" for v in contrib_df["Impact"]
            ]

            fig_bar = go.Figure(
                go.Bar(
                    x=contrib_df["Impact"],
                    y=contrib_df["Feature"],
                    orientation="h",
                    marker=dict(
                        color=bar_colors,
                        line=dict(width=0),
                    ),
                    hovertemplate="%{y}: %{x:+.1f}<extra></extra>",
                )
            )

            fig_bar.update_layout(
                xaxis=dict(
                    title="Impact on Score",
                    gridcolor="rgba(148,163,184,0.08)",
                    zerolinecolor="rgba(148,163,184,0.2)",
                    titlefont=dict(size=11, color="#64748b"),
                ),
                yaxis=dict(title=None),
                margin=dict(l=10, r=20, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8", size=11),
                height=320,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

else:
    with col_results:
        st.markdown(
            """
<div class='metric-card' style='text-align:center; padding:3rem 2rem;'>
    <p style='font-size:2.5rem; margin:0;'>\U0001f50d</p>
    <p style='color:#94a3b8; font-size:1rem; margin:0.5rem 0 0.25rem 0;'>
        No scan results yet
    </p>
    <p style='color:#64748b; font-size:0.85rem; margin:0;'>
        Adjust parameters in the sidebar, then click <strong style='color:#00d084;'>RUN SCAN</strong> to assess organ viability.
    </p>
</div>""",
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────
# Live waveform (always visible)
# ──────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#64748b; font-size:0.78rem; text-transform:uppercase; "
    "letter-spacing:0.08em; font-weight:600;'>Live Ultrasound Signal Feed (Simulated)</p>",
    unsafe_allow_html=True,
)

t = np.linspace(0, 10, 500)
amp = max(0.2, stiffness / 8.0)
freq = 3.0 + ri * 2.0
wave = amp * np.sin(2 * np.pi * freq * t) + np.random.normal(0, 0.05, 500)

fig_wave = go.Figure(
    go.Scatter(
        x=t,
        y=wave,
        mode="lines",
        line=dict(color="#00d084", width=1),
        hoverinfo="skip",
    )
)
fig_wave.update_layout(
    height=120,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-3, 3],
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_wave, use_container_width=True)
