import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
import requests

# --- Page Config ---
st.set_page_config(
    page_title="UltraViab | Organ Viability",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Dark Theme CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* ===== Color Palette ===== */
    :root {
        --bg-deep: #050508;
        --bg-primary: #0c0c10;
        --bg-elevated: #14141a;
        --bg-card: #1c1c24;
        --border: #71718a;          /* Lightened Border */
        --border-light: #8b8ba3;
        --text-bright: #ffffff;
        --text-primary: #ffffff;
        --text-secondary: #f0f0f5;  /* Maximized Contrast */
        --text-muted: #dadae6;      /* Maximized Contrast */
        --accent: #22c55e;
        --accent-dim: rgba(34, 197, 94, 0.2);
        --accent-glow: rgba(34, 197, 94, 0.5);
        --danger: #ef4444;
        --warning: #eab308;
    }
    /* ===== Background ===== */
    [data-testid="stAppViewContainer"] {
        background: var(--bg-deep);
        background-image: 
            radial-gradient(ellipse 100% 80% at 20% 0%, rgba(34, 197, 94, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse 80% 60% at 80% 100%, rgba(59, 130, 246, 0.06) 0%, transparent 50%);
    }
    
    [data-testid="stHeader"] { background: transparent !important; }
    
    /* ===== Typography ===== */
    html, body, [class*="css"] {
        font-family: 'DM Sans', -apple-system, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }
    
    h1 { 
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-bright) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
    }
    
    h2, h3, h4 { 
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    p, span, label, .stMarkdown {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-secondary) !important;
        font-size: 0.95rem !important; /* Slightly larger */
    }
    
    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-deep) 100%) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-bright) !important; /* Maximized contrast */
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
    }
    
    /* ===== Better Sliders ===== */
    .stSlider {
        padding: 0.5rem 0 !important;
    }
    
    .stSlider label {
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* Slider track */
    .stSlider [data-baseweb="slider"] {
        margin-top: 0.5rem;
    }
    
    .stSlider [data-testid="stThumbValue"] {
        background: var(--bg-card) !important;
        color: var(--accent) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        border: 1.5px solid var(--border) !important;
        padding: 0.25rem 0.6rem !important;
        border-radius: 6px !important;
    }
    
    /* Slider min/max values - Ultra Aggressive */
    .stSlider [data-testid="stTickBar"] div,
    .stSlider [data-baseweb="slider"] div {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }
    
    /* Ensure the actual strings like "0" and "100" are caught */
    .stSlider [data-testid="stTickBar"] {
        color: #ffffff !important;
    }


    

    
    /* ===== Selectbox ===== */
    .stSelectbox > div > div {
        font-family: 'DM Sans', sans-serif !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* ===== Expanders ===== */
    .streamlit-expanderHeader {
        font-family: 'DM Sans', sans-serif !important;
        background: var(--bg-elevated) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* ===== Dividers ===== */
    hr { border: none !important; border-top: 1px solid var(--border) !important; }
    
    /* ===== Hide Branding ===== */
    #MainMenu, footer { visibility: hidden; }
    
    /* ===== Buttons ===== */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        background: linear-gradient(135deg, var(--accent) 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 20px var(--accent-dim), 0 0 0 0 var(--accent-glow) !important;
    }

    /* Force primary button to match */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent) 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        border: none !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important; /* Enhanced Contrast */
        font-weight: 700 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px var(--accent-glow), 0 0 20px var(--accent-dim) !important;
        color: #ffffff !important;
    }
    
    /* ===== Chart Container ===== */
    .chart-container {
        background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-elevated) 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    /* ===== Custom Components ===== */
    .metric-card {
        background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-elevated) 100%);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        opacity: 0.5;
    }
    
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-muted);
        font-size: 0.7rem;      /* Increased */
        font-weight: 600;       /* Added weight */
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-bright);
        font-size: 2.2rem;      /* Slightly larger */
        font-weight: 700;
        line-height: 1;
    }
    
    .metric-desc {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-secondary); /* Brightened further */
        font-size: 0.8rem;      /* Increased */
        font-weight: 500;
        margin-top: 0.35rem;
    }
    
    .status-accept { color: var(--accent) !important; text-shadow: 0 0 20px var(--accent-dim); }
    .status-marginal { color: var(--warning) !important; }
    .status-decline { color: var(--danger) !important; }
    
    /* ===== Alert ===== */
    .alert-box {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .alert-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    
    .alert-content h4 {
        color: var(--text-primary);
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0;
    }
    
    .alert-content p {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin: 0.25rem 0 0 0;
    }
    
    /* ===== Signal Monitor (Prominent) ===== */
    .signal-panel {
        background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-elevated) 100%);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .signal-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent 0%, var(--accent) 50%, transparent 100%);
    }
    
    .signal-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    .signal-dot {
        width: 10px;
        height: 10px;
        background: var(--accent);
        border-radius: 50%;
        animation: pulse 1.5s ease-in-out infinite;
        box-shadow: 0 0 12px var(--accent-glow);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(0.85); }
    }
    
    .signal-title {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-primary);
        font-size: 1rem;
        font-weight: 600;
    }
    
    .signal-stats {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent);
        font-size: 0.75rem;
        margin-left: auto;
        background: var(--accent-dim);
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
    }

</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def hex_to_rgba(hex_code, opacity=1.0):
    hex_code = hex_code.lstrip('#')
    r, g, b = int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)
    return f"rgba({r}, {g}, {b}, {opacity})"

# Initialize Session State
if 'organ_type' not in st.session_state:
    st.session_state['organ_type'] = "Kidney"
if 'scan_triggered' not in st.session_state:
    st.session_state['scan_triggered'] = False

def trigger_scan():
    st.session_state['scan_triggered'] = True

# --- Sidebar ---
with st.sidebar:
    st.markdown("### Configuration")
    
    with st.expander("Organ Metadata", expanded=True):
        organ_type = st.selectbox("Organ Type", ["Kidney", "Liver", "Heart", "Lung"], key="organ_type")
        donor_age = st.slider("Donor Age", 0, 100, 45, key="donor_age")
        cit_hours = st.slider("Cold Ischemia Time (hrs)", 0.0, 40.0, 12.0, 0.5, key="cit_hours")
        kdpi = st.slider("KDPI / DRI (%)", 0, 100, 40, key="kdpi")
        cause_death = st.selectbox("Cause of Death", ["Trauma", "Anoxia", "CVA", "Other"], key="cause_death")

    with st.expander("Ultrasound Metrics", expanded=True):
        stiffness = st.slider("Tissue Stiffness (kPa)", 0.0, 30.0, 5.2, 0.1, key="stiffness")
        ri = st.slider("Resistive Index (RI)", 0.0, 1.2, 0.65, 0.01, key="ri")
        swv = st.slider("Shear Wave Velocity (m/s)", 0.0, 5.0, 2.1, 0.1, key="swv")
        perfusion = st.slider("Perfusion Uniformity (%)", 0, 100, 85, key="perfusion")
        echogenicity = st.slider("Echogenicity Grade", 1, 5, 2, key="echogenicity")
        edema = st.slider("Edema Index", 0, 10, 2, key="edema")
        warm_ischemia = st.slider("Warm Ischemia Time (min)", 0, 120, 15, key="warm_ischemia")

# --- Main Content ---

# Header with scan button
header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown("# UltraViab")
    st.caption("AI-Powered Organ Viability Assessment")
with header_right:
    st.markdown("")  # Spacer
    run_scan = st.button("▶  Analyze", key="scan_btn", type="primary", use_container_width=True)

st.divider()

# Check if scan should run
if run_scan or st.session_state.get('scan_triggered', False):
    st.session_state['scan_triggered'] = False
    
    with st.spinner("Analyzing..."):
        time.sleep(0.8)
        
        # API Integration
        api_url = "http://localhost:8000/predict"
        payload = {
            "organ_type": organ_type, "tissue_stiffness_kpa": stiffness,
            "resistive_index": ri, "shear_wave_velocity_ms": swv,
            "perfusion_uniformity_pct": perfusion, "echogenicity_grade": echogenicity,
            "edema_index": edema, "cold_ischemia_hours": cit_hours,
            "donor_age": donor_age, "kdpi_percentile": kdpi,
            "cause_of_death": cause_death, "warm_ischemia_minutes": warm_ischemia
        }
        
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                score = data['viability_score']
                status = data['classification'].upper()
                risk_factors = data.get('risk_factors', [])
                msg = f"Detected risks: {', '.join(risk_factors)}" if risk_factors else "No significant risks detected"
            else:
                score, status, msg = 0, "ERROR", "API connection failed"
        except:
            # Fallback simulation
            score = 100
            score -= (stiffness - 5.0) * 3 if stiffness > 6.0 else 0
            score -= (ri - 0.7) * 40 if ri > 0.7 else 0
            score -= (cit_hours - 12) * 1.5 if cit_hours > 12 else 0
            score -= (donor_age - 50) * 0.3 if donor_age > 50 else 0
            score = max(0, min(100, score))
            
            if score >= 70: status = "ACCEPT"
            elif score >= 40: status = "MARGINAL"
            else: status = "DECLINE"
            msg = "Running in simulation mode"

    # Color mapping
    status_colors = {"ACCEPT": "#22c55e", "MARGINAL": "#eab308", "DECLINE": "#ef4444", "ERROR": "#ef4444"}
    status_classes = {"ACCEPT": "status-accept", "MARGINAL": "status-marginal", "DECLINE": "status-decline"}
    alert_icons = {"ACCEPT": "✓", "MARGINAL": "!", "DECLINE": "✕"}
    alert_bg = {"ACCEPT": "rgba(34,197,94,0.15)", "MARGINAL": "rgba(234,179,8,0.15)", "DECLINE": "rgba(239,68,68,0.15)"}
    color = status_colors.get(status, "#9898a8")
    status_class = status_classes.get(status, "")

    # Metric Cards Row
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Viability Score</div>
            <div class="metric-value" style="color: {color};">{int(score)}</div>
            <div class="metric-desc">Overall assessment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Classification</div>
            <div class="metric-value {status_class}">{status}</div>
            <div class="metric-desc">Transplant decision</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Organ Type</div>
            <div class="metric-value" style="font-size: 1.5rem;">{organ_type}</div>
            <div class="metric-desc">Donor age: {donor_age}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CIT</div>
            <div class="metric-value" style="font-size: 1.5rem;">{cit_hours}h</div>
            <div class="metric-desc">Cold ischemia</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Alert
    alert_titles = {"ACCEPT": "Proceed with transplant", "MARGINAL": "Additional evaluation recommended", "DECLINE": "Does not meet viability standards"}
    st.markdown(f"""
    <div class="alert-box">
        <div class="alert-icon" style="background: {alert_bg.get(status, 'rgba(152,152,168,0.15)')}; color: {color};">
            {alert_icons.get(status, '?')}
        </div>
        <div class="alert-content">
            <h4>{alert_titles.get(status, 'Unknown Status')}</h4>
            <p>{msg}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Charts Row
    st.markdown("### Detailed Analysis")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
    
    with c1:
        categories = ['Stiffness', 'RI', 'CIT', 'Age', 'Perfusion', 'SWV']
        values = [
            min(1, stiffness / 15.0), min(1, ri / 1.0), min(1, cit_hours / 40.0),
            min(1, donor_age / 100.0), min(1, (100-perfusion)/100.0), min(1, swv / 4.0)
        ]
        
        # Close the loop for radar chart
        categories = categories + [categories[0]]
        values = values + [values[0]]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=categories, fill='toself',
            line_color=color, fillcolor=hex_to_rgba(color, 0.12), line_width=2
        ))
        
        ref_values = [0.4, 0.6, 0.5, 0.6, 0.2, 0.5]
        ref_values = ref_values + [ref_values[0]]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=ref_values, theta=categories,
            line_color='rgba(255, 255, 255, 0.8)', line_dash='dash', line_width=2
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, showticklabels=False, range=[0, 1], gridcolor='rgba(45, 45, 58, 0.6)'),
                angularaxis=dict(gridcolor='rgba(45, 45, 58, 0.6)', tickfont=dict(color='#9898a8', size=11, family='DM Sans'))
            ),
            showlegend=False, margin=dict(l=50, r=50, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#9898a8", family="DM Sans"), height=260
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    with c2:
        contribs = {
            "Stiffness": -max(0, (stiffness - 5.0) * 3),
            "RI": -max(0, (ri - 0.7) * 40),
            "CIT": -max(0, (cit_hours - 12) * 1.5),
            "Age": -max(0, (donor_age - 50) * 0.3),
            "Perfusion": 10 if perfusion > 80 else -5
        }
        contrib_df = pd.DataFrame(list(contribs.items()), columns=['Feature', 'Impact'])
        contrib_df = contrib_df.sort_values('Impact', ascending=True)
        
        fig_bar = go.Figure(go.Bar(
            x=contrib_df['Impact'], y=contrib_df['Feature'], orientation='h',
            marker=dict(color=contrib_df['Impact'].apply(lambda x: '#ef4444' if x < 0 else '#22c55e')),
            text=contrib_df['Impact'].apply(lambda x: f"{x:+.1f}"),
            textposition='outside', textfont=dict(color='#9898a8', size=10, family='JetBrains Mono')
        ))
        fig_bar.update_layout(
            xaxis=dict(title="Impact", titlefont=dict(color='#9898a8', size=11), tickfont=dict(color='#9898a8', size=10),
                       gridcolor='rgba(45, 45, 58, 0.4)', zerolinecolor='rgba(45, 45, 58, 0.8)'),
            yaxis=dict(title=None, tickfont=dict(color='#e8e8ed', size=11)),
            margin=dict(l=20, r=50, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=260, bargap=0.35
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

else:
    # Idle state - show placeholder
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.2;">◇</div>
        <h3 style="color: #e8e8ed; font-weight: 600; margin-bottom: 0.5rem;">Ready to Analyze</h3>
        <p style="color: #68687a; font-size: 0.9rem;">Configure parameters in the sidebar, then click Analyze.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Prominent Signal Monitor ---
st.markdown("")
st.markdown("")

freq_val = round(3.0 + (ri * 2.0), 1)
amp_val = round(max(0.3, stiffness / 8.0), 2)

st.markdown(f"""
<div class="signal-panel">
    <div class="signal-header">
        <div class="signal-dot"></div>
        <span class="signal-title">Live Ultrasound Signal</span>
        <span class="signal-stats">FREQ {freq_val} Hz • AMP {amp_val}</span>
    </div>
</div>
""", unsafe_allow_html=True)

t = np.linspace(0, 12, 1200)
amp = amp_val
freq = freq_val
wave = amp * np.sin(2 * np.pi * freq * t) * (1 - 0.02 * t) + np.random.normal(0, 0.015, 1200)

fig_wave = go.Figure()

# Glow layer
fig_wave.add_trace(go.Scatter(
    x=t, y=wave, mode='lines', 
    line=dict(color='rgba(34, 197, 94, 0.25)', width=8),
    hoverinfo='skip'
))

# Main signal
fig_wave.add_trace(go.Scatter(
    x=t, y=wave, mode='lines', 
    line=dict(color='#22c55e', width=2),
    fill='tozeroy', fillcolor='rgba(34, 197, 94, 0.06)',
    hoverinfo='skip'
))

fig_wave.update_layout(
    height=150, 
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, fixedrange=True),
    yaxis=dict(showgrid=False, showticklabels=False, range=[-2.5, 2.5], zeroline=False, fixedrange=True),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False
)
st.plotly_chart(fig_wave, use_container_width=True, config={'displayModeBar': False})
