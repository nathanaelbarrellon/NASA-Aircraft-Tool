import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")

# --- HEADER SECTION ---
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
                Aircraft Performance Visualizations
            </p>
            <p style='
                color: #cccccc; 
                font-size: 0.95rem; 
                margin-top: 0.5rem;
                text-align: left;'>
                Interactive visualizations and sensitivity analysis of aircraft performance.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("https://www.nasa.gov/wp-content/themes/nasa/assets/images/nasa-logo.svg", width=120)

st.markdown("<hr style='margin-top:1rem; border: 1px solid #333;'>", unsafe_allow_html=True)


# --- LOAD DATA FROM MAIN PAGE ---
if 'initial_data' in st.session_state and 'weights' in st.session_state and 'topsis_results' in st.session_state:
    initial_data = st.session_state.initial_data
    weights = st.session_state.weights
    results = st.session_state.topsis_results

    # --- REMOVE TOPSIS SCORE COLUMN ---
    if "TOPSIS Score" in initial_data.columns:
        initial_data = initial_data.drop(columns=["TOPSIS Score"])

    # --- MAIN SECTION ---
    st.header("Aircraft Characteristics")
    if isinstance(initial_data, pd.DataFrame):
        # Get top 10 ranked aircraft
        top_alternatives = results.index[:10].tolist()

        # Select which to compare
        selected_alternatives = st.multiselect(
            "Select aircraft to compare:",
            options=top_alternatives,
            default=top_alternatives[:3],
            format_func=lambda x: f"{x} (TOPSIS Rank: {results.index.get_loc(x)+1})"
        )

        if selected_alternatives:
            # --- CRITERIA ---
            criteria = initial_data.columns.tolist()

            # --- NORMALIZE DATA FOR RADAR ---
            normalized = initial_data.copy().astype(float)
            for col in criteria:
                min_val, max_val = normalized[col].min(), normalized[col].max()
                if max_val > min_val:
                    normalized[col] = (normalized[col] - min_val) / (max_val - min_val)
                else:
                    normalized[col] = 0.5  # constant if no variation

            # --- RADAR CHART ---
            fig_radar = go.Figure()

            for alt in selected_alternatives:
                r = normalized.loc[alt].tolist()
                r_closed = r + [r[0]]
                theta_closed = criteria + [criteria[0]]

                real_values = [initial_data.loc[alt, c] for c in criteria]
                real_text = []
                for v in real_values:
                    if isinstance(v, (int, np.integer)):
                        real_text.append(f"{int(v):,}")
                    elif isinstance(v, (float, np.floating)):
                        if abs(v) >= 1000:
                            real_text.append(f"{v:,.0f}")
                        elif abs(v) >= 1:
                            real_text.append(f"{v:.2f}")
                        else:
                            real_text.append(f"{v:.3f}")
                    else:
                        real_text.append(str(v))

                fig_radar.add_trace(go.Scatterpolar(
                    r=r_closed,
                    theta=theta_closed,
                    fill='toself',
                    name=f"{alt} (Rank {results.index.get_loc(alt)+1})",
                    mode='lines+markers',
                    marker=dict(size=8),
                    line=dict(width=2),
                    hovertemplate='Criterion: %{theta}<br>Normalized: %{r:.3f}<br>Actual value: %{text}<extra></extra>',
                    text=real_text + [real_text[0]]
                ))

            # --- SINGLE SET OF VALUE LABELS (no duplicates) ---
            for alt in selected_alternatives:
                r = normalized.loc[alt].tolist()
                theta = criteria
                real_values = [initial_data.loc[alt, c] for c in criteria]
                real_text = []
                for v in real_values:
                    if isinstance(v, (int, np.integer)):
                        real_text.append(f"{int(v):,}")
                    elif isinstance(v, (float, np.floating)):
                        if abs(v) >= 1000:
                            real_text.append(f"{v:,.0f}")
                        elif abs(v) >= 1:
                            real_text.append(f"{v:.2f}")
                        else:
                            real_text.append(f"{v:.3f}")
                    else:
                        real_text.append(str(v))

                fig_radar.add_trace(go.Scatterpolar(
                    r=r,
                    theta=theta,
                    mode='text',
                    text=real_text,
                    textposition='top center',
                    textfont=dict(color='rgba(255, 80, 80, 0.9)', size=10, family="Arial Bold"),
                    showlegend=False,
                    hoverinfo='skip',
                ))

            # --- STYLE LAYOUT ---
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(40, 60, 80, 0.25)",
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                        ticktext=["0", "25%", "50%", "75%", "100%"],
                        tickfont=dict(size=12, color="rgba(230,230,230,0.9)"),
                        gridcolor="rgba(200,200,200,0.2)",
                        linecolor="rgba(200,200,200,0.3)",
                        layer="below traces"
                    ),
                    angularaxis=dict(
                        direction="clockwise",
                        tickfont=dict(size=13, color="white"),
                        gridcolor="rgba(200,200,200,0.2)"
                    ),
                ),
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=-0.25,
                    xanchor='center',
                    x=0.5,
                    font=dict(size=13)
                ),
                title=dict(
                    text="Overview of Aircraft Characteristics (Normalized Radar Chart)",
                    font=dict(size=20, color="white"),
                    x=0.5,
                    xanchor='center'
                ),
                margin=dict(t=100, b=100, l=100, r=100),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=850,
            )

            st.plotly_chart(fig_radar, use_container_width=True)

    # --- DETAILED ANALYSIS ---
    st.markdown("---")
    st.subheader("Detailed Criterion Analysis")
    for criterion in criteria:
        fig_detail = px.bar(
            initial_data.loc[selected_alternatives],
            y=criterion,
            title=f"Comparison for {criterion}",
            color_discrete_sequence=['teal'],
        )
        fig_detail.update_layout(
            xaxis_title="Aircraft",
            yaxis_title=criterion
        )
        fig_detail.update_traces(
            text=[f"TOPSIS Rank: {results.index.get_loc(alt)+1}" for alt in selected_alternatives],
            textposition='auto',
        )
        st.plotly_chart(fig_detail, use_container_width=True)

else:
    st.warning("Please run the analysis on the main page first to display the visualizations.")

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
