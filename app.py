
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image

# Load logo
logo = Image.open("s2m-logo.png")

# Load data
df = pd.read_csv("Tracking.csv")
df.columns = df.columns.str.strip()  # Clean column names

# App title/logo
st.image(logo, width=200)

# Session state setup
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login logic
def login():
    with st.form("login_form"):
        st.markdown("## 🔐 Admin Login")
        username = st.text_input("Username", placeholder="Enter username", key="username")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username == "admin" and password == "admin123":
                with st.spinner("Signing in..."):
                    st.success("Login successful!")
                    st.session_state.authenticated = True
            else:
                st.error("Invalid credentials")

# Only show dashboard after login
if not st.session_state.authenticated:
    login()
else:
    page = st.sidebar.selectbox("Navigation", ["Dashboard", "Overview"])

    if page == "Dashboard":
        st.title("📊 Dashboard")

        # Overall HC
        total_employees = df["Emp Id"].nunique()
        total_login_ids = df["Emp Id"].count()
        st.write("Active / Inactive:", df.columns.tolist())
        active_count = df[df["Status"].str.lower() == "active"].shape[0]
        inactive_count = df[df["Status"].str.lower() == "inactive"].shape[0]
        total_charts = df["Chart Count"].sum()
        total_icd = df["ICD"].sum()
        total_pages = df["Pages"].sum()

        st.metric("Total Headcount", total_employees)
        st.metric("Total Login IDs", total_login_ids)
        st.metric("Active Employees", active_count)
        st.metric("Inactive Employees", inactive_count)
        st.metric("Total Charts Processed", total_charts)
        st.metric("Total Pages", total_pages)
        st.metric("Total ICD", total_icd)

        if st.button("Go to Overview"):
            st.session_state.page = "Overview"

    elif page == "Overview" or st.session_state.get("page") == "Overview":
        st.title("📋 Overview")

        # Search
        emp_id = st.text_input("🔍 Search by Emp ID")
        if emp_id:
            result = df[df["Emp ID"].astype(str).str.contains(emp_id)]
        else:
            result = df

        st.dataframe(result)

        # Download button
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Overview')
            output.seek(0)
            return output

        st.download_button(
            label="📥 Download Overview as Excel",
            data=to_excel(result),
            file_name='overview.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
