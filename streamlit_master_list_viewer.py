
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Master List Viewer", layout="wide")
st.title("📋 Master List Viewer")

uploaded_file = st.file_uploader("📤 Upload 'Sung-il Master Tracker' Excel", type=["xlsx"])

if uploaded_file:
    try:
        # Load only the 'Master List' sheet
        df = pd.read_excel(uploaded_file, sheet_name="Master List", header=1)
        df.columns = df.columns.astype(str).str.strip()

        st.success("✅ 'Master List' loaded successfully!")
        st.dataframe(df, use_container_width=True)

        # Optional filter by Region if available
        if "Region" in df.columns:
            region_filter = st.multiselect("Filter by Region", sorted(df["Region"].dropna().unique()))
            if region_filter:
                st.markdown("### 🔍 Filtered Results")
                st.dataframe(df[df["Region"].isin(region_filter)], use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error loading 'Master List': {e}")
