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
# LOAD DATA (DEPLOYMENT SAFE)
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
    ["Overview", "EDA", "Insights & Conclusion"]
)

# =========================================================
# OVERVIEW PAGE
# =========================================================
if page == "Overview":
    st.title("🏥 Healthcare Exploratory Data Analysis")

    st.markdown("""
    ### 📌 Project Overview
    This dashboard performs **Exploratory Data Analysis (EDA)** on a healthcare dataset
    to understand:
    - Patient demographics
    - Medical conditions
    - Admission types
    - Billing patterns

    The goal is to extract meaningful insights that can help hospitals and healthcare
    providers make **data-driven decisions**.
    """)

    st.subheader("📊 Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", df.shape[0])
    col2.metric("Total Features", df.shape[1])
    col3.metric("Avg Billing Amount", f"${df['Billing Amount'].mean():.2f}")

    st.subheader("🔍 Preview of Dataset")
    st.dataframe(df.head())

# =========================================================
# EDA PAGE
# =========================================================
elif page == "EDA":
    st.title("📊 Exploratory Data Analysis")

    # -------- Chart 1: Age Distribution --------
    st.subheader("1️⃣ Age Distribution of Patients")
    fig, ax = plt.subplots()
    sns.histplot(df["Age"], bins=20, kde=True, ax=ax)
    ax.set_xlabel("Age")
    ax.set_ylabel("Number of Patients")
    st.pyplot(fig)

    # -------- Chart 2: Gender Distribution --------
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

    # -------- Chart 3: Medical Condition Count --------
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

    # -------- Chart 4: Admission Type --------
    st.subheader("4️⃣ Admission Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(
