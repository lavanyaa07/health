import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Healthcare EDA Dashboard",
    page_icon="🏥",
    layout="wide"
)

# =========================================================
# LOAD DATA (STREAMLIT CLOUD SAFE)
# =========================================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "healthcare_dataset.csv")
    return pd.read_csv(file_path)

df = load_data()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("🏥 Healthcare Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Exploratory Data Analysis", "Insights & Conclusion"]
)

# =========================================================
# OVERVIEW PAGE
# =========================================================
if page == "Overview":
    st.title("🏥 Healthcare Exploratory Data Analysis")

    st.markdown("""
    ### 📌 Project Overview
    This dashboard performs Exploratory Data Analysis (EDA) on a healthcare dataset
    to understand patient demographics, admission patterns, medical conditions,
    and billing trends.
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Average Billing", f"${df['Billing Amount'].mean():.2f}")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# =========================================================
# EDA PAGE
# =========================================================
elif page == "Exploratory Data Analysis":
    st.title("📊 Exploratory Data Analysis")

    # 1️⃣ Age Distribution
    st.subheader("1️⃣ Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["Age"], bins=20, kde=True, ax=ax)
    ax.set_xlabel("Age")
    ax.set_ylabel("Number of Patients")
    st.pyplot(fig)

    # 2️⃣ Gender Distribution
    st.subheader("2️⃣ Gender Distribution")
    gender_counts = df["Gender"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        gender_counts,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

    # 3️⃣ Medical Condition Distribution
    st.subheader("3️⃣ Medical Conditions Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(
        y="Medical Condition",
        data=df,
        order=df["Medical Condition"].value_counts().index,
        ax=ax
    )
    ax.set_xlabel("Number of Patients")
    ax.set_ylabel("Medical Condition")
    st.pyplot(fig)

    # 4️⃣ Admission Type Distribution
    st.subheader("4️⃣ Admission Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(
        x="Admission Type",
        data=df,
        ax=ax
    )
    ax.set_xlabel("Admission Type")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # 5️⃣ Billing Amount by Insurance Provider
    st.subheader("5️⃣ Average Billing Amount by Insurance Provider")
    billing_avg = (
        df.groupby("Insurance Provider")["Billing Amount"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    billing_avg.plot(kind="bar", ax=ax)
    ax.set_xlabel("Insurance Provider")
    ax.set_ylabel("Average Billing Amount")
    st.pyplot(fig)

# =========================================================
# INSIGHTS & CONCLUSION PAGE
# =========================================================
else:
    st.title("📌 Key Insights & Conclusion")

    st.markdown("""
    ### 🔍 Key Insights
    - Most patients belong to adult and senior age groups.
    - Gender distribution is nearly balanced.
    - A few medical conditions account for a large proportion of hospital visits.
    - Emergency admissions are more frequent than elective ones.
    - Billing amounts vary significantly across insurance providers.

    ### ✅ Conclusion
    This EDA helps understand patient demographics, healthcare demand,
    and billing behavior. These insights can assist hospitals in
    improving patient care, resource planning, and cost management.
    """)

