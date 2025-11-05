import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.express as px
from datetime import datetime


# Configuration of the page
st.set_page_config(page_title="User Guide", page_icon="�", layout="wide")

import streamlit as st


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
                User Guide: Aircraft Design Decision Support Tool
            </p>
            <p style='
                color: #cccccc; 
                font-size: 0.95rem; 
                margin-top: 0.5rem;
                text-align: left;'>
                This tool has been designed by the Vehicle Optimization for Low-Emission Transport Aircraft (VOLTA) team.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("https://www.nasa.gov/wp-content/themes/nasa/assets/images/nasa-logo.svg", width=120)

st.markdown("<hr style='margin-top:1rem; border: 1px solid #333;'>", unsafe_allow_html=True)




#Outline
st.markdown("""
<h2 style='margin-bottom: 0.5rem;'>Outline</h2>
<div style='
    background-color: rgba(255, 255, 255, 0.05);
    padding: 1.2rem 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #00CED1;
    line-height: 1.8;
    font-size: 1.05rem;
'>
    <ol style='margin: 0; padding-left: 1.5rem;'>
        <li><b>What is this tool?</b></li>
        <li><b>How to Use This Tool</b></li>
        <li><b>How to Interpret the Results</b></li>
        <li><b>More Information</b></li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Introduction
st.header("1. What is this tool?")
st.write("""
This tool  helps aircraft designers and decision-makers evaluate and compare different aircraft configurations 
using the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) method. It provides a 
systematic approach to rank different design alternatives based on multiple criteria.
""")

st.markdown("---")

st.markdown("""
<h2 style='margin-bottom: 0.5rem;'>2. How to Use This Tool</h2>
<p style='color:#cccccc;'>
This tool is divided into three main sections:
</p>
""", unsafe_allow_html=True)

# --- THREE COLUMNS CLEANER VISUAL ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background-color:rgba(255,255,255,0.05);
                padding:1rem; border-radius:10px;
                border-left:4px solid #00CED1;'>
        <h4>🏠 Home Page / User Guide</h4>
        <ul>
            <li>Understand the tool's purpose</li>
            <li>Understand the outputs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color:rgba(255,255,255,0.05);
                padding:1rem; border-radius:10px;
                border-left:4px solid #00CED1;'>
        <h4>📊 Input Parameters</h4>
        <ul>
            <li>Alternatives to display</li>
            <li>Type of electrification</li>
            <li>Confidence in projecting tech assumptions</li>
            <li>Time frame</li>
            <li>Aircraft size</li>
            <li>Electric architecture</li>
            <li>Criteria weights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background-color:rgba(255,255,255,0.05);
                padding:1rem; border-radius:10px;
                border-left:4px solid #00CED1;'>
        <h4>📈 Results Visualizations</h4>
        <ul>
            <li>Radar charts</li>
            <li>Compare top performers</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style='
    border: 1.5px solid rgba(0, 206, 209, 0.6);
    border-radius: 12px;
    background-color: rgba(255, 255, 255, 0.02);
    padding: 1.8rem 2rem;
    margin-top: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 0 10px rgba(0, 206, 209, 0.15);
'>
    <h2 style='color:#00CED1; margin-bottom:0.8rem;'> Step-by-Step Process</h2>
    <p>Go to the <b>TOOL</b> page and follow the instructions below.</p>
    <h4>1️⃣ Configure the Initial Simulation Parameters</h4>
    <ul>
        <li>Choose the number of aircraft alternatives to display at the end of the TOPSIS analysis</li>
        <li>Choose the type of electrification (hybrid-electric or full electric) ❌</li>
        <li>Choose the confidence in projecting technology assumptions ❌</li>
        <li>Choose the timeframe desired ❌</li>
        <li>Choose the aircraft size ❌</li>
        <li>Choose the electric architecture ❌</li>
    </ul>
    <p style='color:#999; font-size:0.9rem;'>
        The ❌ symbol refers to buttons present on the tool but not functional at the moment.
    </p>
    <hr style='border:0.3px solid #333; margin:1rem 0;'>
    <h4>2️⃣ Set Criteria Weights</h4>
    <p>Use the sliders to assign importance (1–5) to each criterion:</p>
    <ul>
        <li>Aircraft Cruise Speed</li>
        <li>Total Energy Required</li>
        <li>Direct Operating Cost</li>
        <li>Required Yield</li>
        <li>Acquisition Price</li>
        <li>Trip Fuel</li>
    </ul>
    <p>The weight breakdown is shown on a pie chart to visualize the distribution of importance among criteria.</p>
    <hr style='border:0.3px solid #333; margin:1rem 0;'>
    <h3 style='color:white;'>3️⃣ Run the TOPSIS Analysis</h3>
    <ul>
        <li>Click on the 🚀 <b>Run TOPSIS Analysis</b> button</li>
        <li>Examine the simulated aircraft performance table</li>
        <li>Review the TOPSIS ranking and visualization results</li>
    </ul>
    Once completed, you can explore detailed comparisons on the Vizualisation page
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Section 4
st.header("3. How to interpret the results ?")
st.write(" This part refers to the Vizualisation page")

st.write("""
1. Select the aircraft to compare
2. Compare the results on the Radar Chart
3. Compare each metrics with the others graphs
""")
st.write("It is now possible to make a design descision !")
st.markdown("---")


# Section 4
st.header("4. More Information")
st.write("This part allows to understand the construction of the tool")

st.write("""This tool is based on EDS simulation. Given the long time of run, surrogate models are used to speed up the process. Once the resultst are obtained,  
         there are process on python to perform the TOPSIS analysis and visualize the results.
""")

st.write("""For more information, please contact us at :
         - nbarrellon3@gatech.edu
         - adaveau3@gatech.edu
         - iattafi3@gatech.edu
         - gklinger7@gatech.edu
         - nmirkhelkar7@gatech.edu
         - dshauib3@gatech.edu
         - drobinson321@gatech.edu
         """)



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














