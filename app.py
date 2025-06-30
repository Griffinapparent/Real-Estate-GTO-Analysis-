import streamlit as st
import json
from generate_mock_nyc_properties import generate_properties
from analyze_market_intelligence import analyze_market_intelligence
from gto_decision_engine import generate_gto_recommendations
from generate_gto_pdf_report import create_pdf

st.set_page_config(page_title="GTO Real Estate Strategist", layout="wide")
st.sidebar.title("Settings")

num_properties = st.sidebar.slider("Number of Properties", 5, 50, 10)
neighborhood = st.sidebar.selectbox("NYC Neighborhood", [
    "Midtown Manhattan", "Financial District", "Hudson Yards", "SoHo", "Tribeca", "Chelsea", "Flatiron"
])
strategy_goal = st.sidebar.text_input("Strategy Goal", "maximize risk-adjusted return")
run_button = st.sidebar.button("Run GTO Analysis")

st.title("🏙️ Game Theory Optimal (GTO) Real Estate Analyzer")

if run_button:
    st.subheader("1. Generating Mock NYC Property Data")
    properties = generate_properties(count=num_properties, neighborhood=neighborhood)
    with open("mock_properties.json", "w") as f:
        json.dump(properties, f, indent=2)
    st.success(f"Generated {num_properties} properties in {neighborhood}.")
    st.dataframe(properties[:5])

    st.subheader("2. Analyzing Market Intelligence")
    market_text = analyze_market_intelligence(properties)
    with open("market_analysis.txt", "w") as f:
        f.write(market_text)
    st.text_area("Market Intelligence Analysis", market_text, height=300)

    st.subheader("3. Running GTO Strategy Engine")
    gto_json = generate_gto_recommendations(properties, strategy_goal)
    try:
        gto_recommendations = json.loads(gto_json)
    except Exception as e:
        st.error("Error parsing GTO JSON response")
        st.stop()
    with open("gto_recommendations.json", "w") as f:
        json.dump(gto_recommendations, f, indent=2)
    st.table(gto_recommendations[:5])

    st.subheader("4. Generating PDF Report")
    create_pdf("GTO_Report.pdf")
    with open("GTO_Report.pdf", "rb") as f:
        st.download_button("📄 Download GTO_Report.pdf", f, file_name="GTO_Report.pdf")
