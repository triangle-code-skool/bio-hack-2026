import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
import requests

# --- Page Config ---
st.set_page_config(
    page_title="UltraViab | Organ Viability",
    page_icon="microscope",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        width: 100%;
        background-color: #00d084;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #41424b;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.title("🔬 Scan Inputs")

# Define inputs with keys for session_state access
st.sidebar.subheader("Organ Metadata")
organ_type = st.sidebar.selectbox("Organ Type", ["Kidney", "Liver", "Heart", "Lung"], key="organ_type")
donor_age = st.sidebar.slider("Donor Age", 0, 100, 45, key="donor_age", help="Age of the donor in years")
cit_hours = st.sidebar.slider("Cold Ischemia Time (hrs)", 0.0, 40.0, 12.0, 0.5, key="cit_hours")
kdpi = st.sidebar.slider("KDPI / DRI (%)", 0, 100, 40, key="kdpi", help="Kidney Donor Profile Index")
cause_death = st.sidebar.selectbox("Cause of Death", ["Trauma", "Anoxia", "CVA", "Other"], key="cause_death")

st.sidebar.subheader("Ultrasound Parameters")
# Dynamic ranges based on organ type could be implemented here
stiffness = st.sidebar.slider("Tissue Stiffness (kPa)", 0.0, 30.0, 5.2, 0.1, key="stiffness", help="Normal: 3.8-6.0 (Liver)")
ri = st.sidebar.slider("Resistive Index (RI)", 0.0, 1.2, 0.65, 0.01, key="ri", help="Normal: 0.5-0.7")
swv = st.sidebar.slider("Shear Wave Velocity (m/s)", 0.0, 5.0, 2.1, 0.1, key="swv")
perfusion = st.sidebar.slider("Perfusion Uniformity (%)", 0, 100, 85, key="perfusion", help=">85% is ideal")
echogenicity = st.sidebar.slider("Echogenicity Grade", 1, 5, 2, key="echogenicity", help="1=Homogeneous, 5=Heterogeneous")
edema = st.sidebar.slider("Edema Index", 0, 10, 2, key="edema", help="0=None, 10=Severe")
warm_ischemia = st.sidebar.slider("Warm Ischemia Time (min)", 0, 120, 15, key="warm_ischemia")


# --- Main Content ---
st.title("UltraViab — Non-Invasive Organ Viability Assessment")

# Placeholder for Waveform/Header Image
st.markdown("### Active Scan: `UV-2026-0207` | Status: **Ready**")

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### Action")
    run_scan = st.button("RUN SCAN ▶")
    
    st.markdown("---")
    st.markdown("#### Presets")
    
    # Preset Logic
    def load_preset(preset_name):
        if preset_name == "Healthy Kidney":
            st.session_state.organ_type = "Kidney"
            st.session_state.donor_age = 25
            st.session_state.cit_hours = 6.0
            st.session_state.stiffness = 4.5
            st.session_state.ri = 0.6
            st.session_state.perfusion = 95
            st.session_state.kdpi = 20
        elif preset_name == "Marginal Liver":
            st.session_state.organ_type = "Liver"
            st.session_state.donor_age = 55
            st.session_state.cit_hours = 14.0
            st.session_state.stiffness = 9.0
            st.session_state.ri = 0.75
            st.session_state.perfusion = 75
            st.session_state.kdpi = 65
        elif preset_name == "High-Risk Heart":
            st.session_state.organ_type = "Heart"
            st.session_state.donor_age = 60
            st.session_state.cit_hours = 5.0
            st.session_state.stiffness = 12.0
            st.session_state.ri = 0.9
            st.session_state.perfusion = 50
            st.session_state.kdpi = 80
            st.session_state.edema = 8
        elif preset_name == "The Surprise":
            st.session_state.organ_type = "Kidney"
            st.session_state.donor_age = 62
            st.session_state.cit_hours = 18.0
            st.session_state.kdpi = 92 # High risk!
            st.session_state.stiffness = 4.2 # But scan is Good!
            st.session_state.ri = 0.55
            st.session_state.perfusion = 95
        
        st.toast(f"Preset Loaded: {preset_name}")

    if st.button("Load: Healthy Kidney"):
        load_preset("Healthy Kidney")
        st.rerun()
    if st.button("Load: Marginal Liver"):
        load_preset("Marginal Liver")
        st.rerun()
    if st.button("Load: High-Risk Heart"):
        load_preset("High-Risk Heart")
        st.rerun()
    if st.button("Load: 'The Surprise'"):
        load_preset("The Surprise")
        st.rerun()

# --- Logic & Results ---
if run_scan:
    with st.spinner("Processing Ultrasound Data..."):
        time.sleep(1.2) # Simulate processing
        
        # --- API INTEGRATION ---
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
            "warm_ischemia_minutes": warm_ischemia
        }
        
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                score = data['viability_score']
                status = data['classification']
                # Map status to color
                color_map = {"Accept": "#00d084", "Marginal": "#ffb300", "Decline": "#ff3d3d"}
                color = color_map.get(status, "gray")
                
                # Construct message based on risk factors if available
                risk_factors = data.get('risk_factors', [])
                if risk_factors:
                    msg = f"Notable risks: {', '.join(risk_factors)}."
                else:
                    msg = "No significant risk factors detected."
                    
            else:
                st.error(f"API Error: {response.status_code}")
                # Fallback to mock for demo continuity if API fails
                score = 50
                status = "API ERROR"
                color = "gray"
                msg = "Could not connect to backend."
                
        except Exception as e:
            st.warning(f"Backend Offline ({str(e)}). Using Simulation Mode.")
            # --- FALLBACK MOCK LOGIC ---
            score = 100
            score -= (stiffness - 5.0) * 3 if stiffness > 6.0 else 0
            score -= (ri - 0.7) * 40 if ri > 0.7 else 0
            score -= (cit_hours - 12) * 1.5 if cit_hours > 12 else 0
            score -= (donor_age - 50) * 0.3 if donor_age > 50 else 0
            score -= (100 - perfusion) * 0.2
            score = max(0, min(100, score))
            
            if score >= 70:
                status = "ACCEPT"
                color = "#00d084"
                msg = "Organ shows excellent viability parameters. (SIMULATED)"
            elif score >= 40:
                status = "MARGINAL"
                color = "#ffb300"
                msg = "Organ shows signs of stress. (SIMULATED)"
            else:
                status = "DECLINE"
                color = "#ff3d3d"
                msg = "High risk features detected. (SIMULATED)"

    # --- Display Results ---
    with col2:
        # 1. Score Card
        st.markdown(f"""
        <div class='metric-card' style='border-left: 8px solid {color}; margin-bottom: 20px;'>
            <h2 style='margin:0; color:gray;'>VIABILITY SCORE</h2>
            <h1 style='font-size: 6rem; margin:0; color:{color};'>{int(score)}</h1>
            <h3 style='margin:0; color: white;'>{status} <span style='font-size:1rem; font-weight:normal; color:#aaa;'>(Confidence: 87%)</span></h3>
            <p style='margin-top:10px; color: #ddd;'>{msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Charts Row
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("### Parameter Analysis")
            # Normalization for Radar Chart (Mock ranges)
            categories = ['Stiffness', 'RI', 'CIT', 'Age', 'Perfusion', 'SWV']
            
            # Normalize to 0-1 scale for the chart (approximate max values)
            values = [
                min(1, stiffness / 15.0),
                min(1, ri / 1.0),
                min(1, cit_hours / 40.0),
                min(1, donor_age / 100.0),
                min(1, (100-perfusion)/100.0), # Inverted: higher is worse for this chart logic? No, let's keep it consistent.
                min(1, swv / 4.0)
            ]
            # Actually, standard radar charts usually show "Good" on outside or inside. 
            # Let's assume 0 is good and 1 is bad for this chart? Or vice versa.
            # "Normal Zone" is usually low values for stiffness/RI, but Age is distinct.
            # Let's just plot normalized values and a "Limit" line.
            
            fig_radar = go.Figure()

            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Current Organ',
                line_color=color
            ))
            
            # Add a "Normal/Safe limit" trace
            fig_radar.add_trace(go.Scatterpolar(
                r=[0.4, 0.6, 0.5, 0.6, 0.2, 0.5], # Arbitrary "Normal" thresholds
                theta=categories,
                name='Normal Limit',
                line_color='green',
                line_dash='dash' 
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1])
                ),
                showlegend=True,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white")
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with chart_col2:
            st.markdown("### Risk Factors")
            # Feature Contributions (Mock)
            # Negative means "Pulls score down" (Risk), Positive means "Pulls score up" (Benefit)
            
            # Calculate simple contributions based on the penalty logic
            contribs = {
                "Stiffness": -1 * max(0, (stiffness - 5.0) * 3),
                "RI": -1 * max(0, (ri - 0.7) * 40),
                "CIT": -1 * max(0, (cit_hours - 12) * 1.5),
                "Age": -1 * max(0, (donor_age - 50) * 0.3),
                "Perfusion": 10 if perfusion > 80 else -5
            }
            
            # Filter to non-zero or top factors
            contrib_df = pd.DataFrame(list(contribs.items()), columns=['Feature', 'Impact'])
            contrib_df = contrib_df.sort_values('Impact', ascending=True)
            
            fig_bar = go.Figure(go.Bar(
                x=contrib_df['Impact'],
                y=contrib_df['Feature'],
                orientation='h',
                marker=dict(
                    color=contrib_df['Impact'].apply(lambda x: '#ff3d3d' if x < 0 else '#00d084')
                )
            ))
            
            fig_bar.update_layout(
                xaxis_title="Impact on Viability Score",
                yaxis_title=None,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

else:
    with col2:
        st.info("Adjust parameters in the sidebar and click 'RUN SCAN' to see viability assessment.")

# --- Live Waveform (Visual Only) ---
st.markdown("---")
st.markdown("#### Live Ultrasound Signal Feed (Simulated)")

# Generate synthetic wave based on parameters
t = np.linspace(0, 10, 500)
# Stiffness affects amplitude, RI affects frequency slightly
amp = max(0.2, stiffness / 8.0) 
freq = 3.0 + (ri * 2.0)
wave = amp * np.sin(2 * np.pi * freq * t) + np.random.normal(0, 0.05, 500)

fig_wave = go.Figure(data=go.Scatter(x=t, y=wave, mode='lines', line=dict(color='#00d084', width=1)))
fig_wave.update_layout(
    height=150,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(showgrid=False, showticklabels=False),
    yaxis=dict(showgrid=False, showticklabels=False, range=[-3, 3]),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#0e1117'
)
st.plotly_chart(fig_wave, use_container_width=True)
