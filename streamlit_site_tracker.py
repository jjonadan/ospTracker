
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="OSP Site Tracker", layout="wide")
st.title("📍 OSP Site Tracker (Web Version)")

if "remarks_data" not in st.session_state:
    st.session_state.remarks_data = {}

# Upload the Excel tracker
uploaded_file = st.file_uploader("📤 Upload 'SUNGIL_OSP Acceptance Tracker' Excel", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="SUNGIL_OSP Acceptance Tracker", skiprows=4)
        df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
        df = df.dropna(subset=["Site Name", "PLA ID"]).copy()

        st.success("✅ File uploaded successfully!")
        st.markdown("### 🔍 Filtered Site List")

        region_filter = st.multiselect("Filter by Region", sorted(df["Region"].dropna().unique()))
        filtered_df = df[df["Region"].isin(region_filter)] if region_filter else df

        for idx, row in filtered_df.iterrows():
            with st.expander(f"📌 {row['Site Name']} ({row['Region']})"):
                st.write(f"**PLA ID:** {row['PLA ID']}")
                st.write(f"**PAT Target:** {row.get('PAT TARGET', 'N/A')}")
                st.write(f"**PAC Target:** {row.get('PAC TARGET', 'N/A')}")
                st.write(f"**FAC Target:** {row.get('FAC TARGET', 'N/A')}")
                site_key = str(row["PLA ID"])

                st.markdown("#### ✍ Add Remark")
                new_remark = st.text_area("New Remark", key=f"remark_input_{site_key}")
                date = st.date_input("Date", value=datetime.date.today(), key=f"date_input_{site_key}")

                if st.button("➕ Add Remark", key=f"add_btn_{site_key}") and new_remark.strip():
                    if site_key not in st.session_state.remarks_data:
                        st.session_state.remarks_data[site_key] = []
                    st.session_state.remarks_data[site_key].append({"date": str(date), "remark": new_remark.strip()})
                    st.success("✅ Remark added.")

                st.markdown("#### 🕒 Remark History")
                if site_key in st.session_state.remarks_data:
                    for entry in reversed(st.session_state.remarks_data[site_key]):
                        st.info(f"{entry['date']} - {entry['remark']}")
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
