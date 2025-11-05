import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="TOPSIS Dashboard", page_icon="✈️", layout="wide")

# Deux colonnes : texte à gauche, logo à droite
col1, col2 = st.columns([5, 1])

with col1:
    st.markdown("""
        <div style='text-align:left;'>
            <p style='
                font-size: 2.5rem; 
                font-weight: 700; 
                color: white; 
                margin-bottom: 0;
                white-space: nowrap;'>
                Multi-Criteria Decision Making Tool
            </p>
            <p style='
                color: #cccccc; 
                font-size: 0.95rem; 
                margin-top: 0.5rem;
                text-align: left;'>
                Interactive multi-criteria analysis using the TOPSIS method to rank simulated aircraft performance.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("https://www.nasa.gov/wp-content/themes/nasa/assets/images/nasa-logo.svg", width=120)

st.markdown("<hr style='margin-top:1rem; border: 1px solid #333;'>", unsafe_allow_html=True)

# --- FIX Pandas Styler rendering limit for large DataFrames ---
pd.set_option("styler.render.max_elements", 5_000_000)

# --- GENERAL INPUTS ---
st.header("Simulation Parameters")

col1, col2, col3, col4 = st.columns(4)

n_alternatives = 1000  # fixed value instead of user input
with col1:
    top_n = st.number_input("Top alternatives to display", min_value=1, max_value=n_alternatives, value=10)
with col2:
    electrif = st.selectbox("Electrification - Unfunctional", ["None", "Hybrid", "Full Electric"])
with col3:
    passengers = st.selectbox("Aircraft size (pax)", [8, 20, 50, 70, 100, 150, 210, 300])
with col4:
    architecture = st.multiselect("Electric Architecture - Unfunctionnal", ["Series", "Parallel", "Turboelectric"])

col5, col6 = st.columns(2)
with col5:
    tech_orient = st.radio("Confidence in projecting technology assumptions - Unfunctional", ["Conservative", "Aggressive", "Nominal"])
with col6:
    timeframe = st.radio("Time frame desired - Unfunctional", ["2035", "2045", "2055"])

st.markdown("---")


# --- CRITERIA ---
inputs_with_units = [
    "Aircraft Cruise Speed (knots)",
    "Total Energy Required (MJ)",
    "Direct operating cost plus interest ($/mile)",
    "Required yield per revenue passenger mile ($/mile)",
    "Acquisition price with spares ($M)",
    "Trip Fuel (kg)"
]

inputs = [
    "Aircraft Cruise Speed",
    "Total Energy Required",
    "Direct operating cost plus interest",
    "Required yield per revenue passenger mile",
    "Acquisition price with spares",
    "Trip Fuel"
]

st.header("Criteria Weights")

# --- TWO COLUMNS: input weights + pie chart ---
col_inputs, col_chart = st.columns([3, 2])

with col_inputs:
    weights = {}
    for inp in inputs:
        weight_value = st.slider(
            f"Weight: {inp}",
            min_value=0,
            max_value=5,
            value=3,
            step=1,
            key=f"weight_{inp}"
        )
        weights[inp] = weight_value

    # Normalisation
    total_raw_weight = sum(weights.values())
    normalized_weights = {k: v / total_raw_weight for k, v in weights.items()}
    weights = normalized_weights

with col_chart:
    st.markdown("<h3 style='text-align: center;'>Weight Distribution</h3>", unsafe_allow_html=True)

    weights_df = pd.DataFrame({
        "Criteria": list(weights.keys()),
        "Weight": list(weights.values())
    }).sort_values(by="Weight", ascending=False)

    fig = px.pie(
        weights_df,
        names="Criteria",
        values="Weight",
        hole=0.55,
        color_discrete_sequence=px.colors.sequential.Tealgrn_r
    )

    fig.update_traces(
        textinfo="percent",
        textposition="inside",
        insidetextfont=dict(size=15, color="white"),
        hovertemplate="<b>%{label}</b><br>Weight: %{value:.2f} (%{percent})<extra></extra>",
        pull=[0.05 if w == weights_df["Weight"].max() else 0 for w in weights_df["Weight"]],
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=13, color="white"),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(t=20, b=50, l=0, r=0),
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

# --- DEFINE OPTIMIZATION TYPE (MAX/MIN) ---
optimization = {
    inputs_with_units[0]: "max",
    inputs_with_units[1]: "min",
    inputs_with_units[2]: "min",
    inputs_with_units[3]: "min",
    inputs_with_units[4]: "min",
    inputs_with_units[5]: "min"
}

st.markdown("---")

# --- RUN TOPSIS ANALYSIS ---
if st.button("🚀 Run TOPSIS Analysis"):
    # --- SIMULATED DATA ---
    data = {"Case": [f"Aircraft {i+1}" for i in range(n_alternatives)]}
    for i, criterion in enumerate(inputs_with_units):
        if i == 0:
            data[criterion] = [random.randint(210, 250) for _ in range(n_alternatives)]
        elif i == 1:
            data[criterion] = [round(random.uniform(3, 7), 3) for _ in range(n_alternatives)]
        elif i == 2:
            data[criterion] = [round(random.uniform(6.4, 8.7), 3) for _ in range(n_alternatives)]
        elif i == 3:
            data[criterion] = [round(random.uniform(1.35, 1.5), 3) for _ in range(n_alternatives)]
        elif i == 4:
            data[criterion] = [round(random.uniform(220, 270), 3) for _ in range(n_alternatives)]
        elif i == 5:
            data[criterion] = [random.randint(27032, 31032) for _ in range(n_alternatives)]

    df = pd.DataFrame(data)

    st.subheader(f"Simulated Aircraft Data ({n_alternatives} alternatives, {passengers} passengers)")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- NORMALIZATION ---
    df_norm = df.copy()
    for inp in inputs_with_units:
        norm = np.linalg.norm(df[inp])
        df_norm[inp] = df[inp] / norm if norm != 0 else df[inp]

    # --- APPLY WEIGHTS ---
    df_weighted = df_norm.copy()
    for inp, weight_inp in zip(inputs_with_units, inputs):
        df_weighted[inp] *= weights[weight_inp]

    # --- IDEAL / ANTI-IDEAL SOLUTIONS ---
    ideal = {inp: df_weighted[inp].max() if optimization[inp] == "max" else df_weighted[inp].min() for inp in inputs_with_units}
    anti_ideal = {inp: df_weighted[inp].min() if optimization[inp] == "max" else df_weighted[inp].max() for inp in inputs_with_units}

    # --- DISTANCES & TOPSIS SCORES ---
    D_plus, D_minus = [], []
    for i in range(n_alternatives):
        d_plus = np.sqrt(sum((df_weighted.loc[i, inp] - ideal[inp]) ** 2 for inp in inputs_with_units))
        d_minus = np.sqrt(sum((df_weighted.loc[i, inp] - anti_ideal[inp]) ** 2 for inp in inputs_with_units))
        D_plus.append(d_plus)
        D_minus.append(d_minus)

    df["TOPSIS Score"] = [d_minus / (d_plus + d_minus) for d_plus, d_minus in zip(D_plus, D_minus)]
    df_sorted = df.sort_values(by="TOPSIS Score", ascending=False).reset_index(drop=True)
    topN = df_sorted.head(int(top_n))

    # --- HIGHLIGHT BEST ---
    def highlight_best_row(row):
        color = "background-color: #3CB371; color: white" if row.name == 0 else ""
        return [color] * len(row)

    st.markdown("---")
    st.session_state['initial_data'] = df.set_index('Case')
    st.session_state['topsis_results'] = df_sorted.set_index('Case')
    st.session_state['weights'] = weights

    st.subheader(f"TOPSIS Ranking (Top {int(top_n)} Aircraft)")
    st.dataframe(topN.style.apply(highlight_best_row, axis=1), use_container_width=True)

    # --- VISUALIZATION ---
    st.markdown(f"### Top {int(top_n)} Aircraft - TOPSIS Scores")
    fig = px.bar(
        topN.sort_values(by="TOPSIS Score", ascending=False),
        x="Case",
        y="TOPSIS Score",
        text="TOPSIS Score",
        color="TOPSIS Score",
        color_continuous_scale=px.colors.sequential.Tealgrn,
    )
    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>TOPSIS Score: %{y:.4f}<extra></extra>"
    )
    fig.update_layout(
        xaxis=dict(categoryorder="array", categoryarray=topN["Case"]),
        yaxis_title="Score",
        xaxis_title="Aircraft Case",
        height=450,
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=13),
    )
    st.plotly_chart(fig, use_container_width=True)

    best_alt = topN.iloc[0]["Case"]
    best_score = topN.iloc[0]["TOPSIS Score"]
    st.success(f"✅ **Best aircraft configuration:** {best_alt} — TOPSIS Score: {best_score:.4f}")

else:
    st.info("Click **🚀 Run TOPSIS Analysis** to generate simulated aircraft data and compute the ranking.")

st.markdown("---")
# --- FOOTER SECTION WITH LOGO ---
col_footer_left, col_footer_right = st.columns([4, 1])

with col_footer_left:
    st.caption(f"Streamlit Prototype - last update {datetime.now().strftime('%d %B %Y - %H:%M')}")

with col_footer_right:
    st.markdown(
        """
        <div style='text-align: right; margin-top: -25px;'>
            <img src='https://www.asdl.gatech.edu/images/hero/ASDL-Icon-sketchy-blue%2Bgold.gif' width='150'>
        </div>
        """,
        unsafe_allow_html=True
    )

