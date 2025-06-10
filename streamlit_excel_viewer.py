
import streamlit as st
import pandas as pd

st.set_page_config(page_title="OSP Tracker Viewer", layout="wide")
st.title("📊 OSP Tracker Viewer (Excel Raw View)")

uploaded_file = st.file_uploader("📤 Upload Tracker Excel", type=["xlsx"])

if uploaded_file:
    try:
        # Try to read without skipping rows
        df = pd.read_excel(uploaded_file, sheet_name="SUNGIL_OSP Acceptance Tracker", header=1)
        df.columns = df.columns.astype(str).str.strip()

        st.success("✅ File loaded successfully!")
        st.markdown("### 📋 Full Data View")
        st.dataframe(df, use_container_width=True)

        # Optional filter
        if "Region" in df.columns:
            region_filter = st.multiselect("Filter by Region", sorted(df["Region"].dropna().unique()))
            if region_filter:
                st.markdown("### 🔍 Filtered Results")
                st.dataframe(df[df["Region"].isin(region_filter)], use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error loading Excel: {e}")
