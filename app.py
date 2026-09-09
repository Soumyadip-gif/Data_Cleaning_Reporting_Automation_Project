import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.cleaning import clean_data
from modules.validation import validate_data
from modules.report import generate_excel_report
from modules.analysis import (
    calculate_kpis,
    numeric_summary,
    categorical_summary,
    column_analysis,
    generate_insights
)
# from modules.visualization import (
#     create_region_chart,
#     create_category_chart,
#     create_product_chart
#)

# Page configuration
st.set_page_config(
    page_title="Data Cleaning & Reporting Automation",
    page_icon="📊",
    layout="wide"
)
import time

with st.spinner("🚀 Loading Data Cleaning & Reporting Automation..."):
    time.sleep(1.5)

# Custom CSS
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0e1117, #161b22);
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #aab2bf;
        margin-bottom: 35px;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        transition: transform 0.25s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        padding: 12px;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
    }

    /* File uploader */
    section[data-testid="stFileUploader"] {
        border-radius: 15px;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        border-radius: 10px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    '<div class="main-title">📊 Data Cleaning & Reporting Automation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Automate data cleaning, validation, analysis, visualization, and reporting.'
    '</div>',
    unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Load dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Dataset uploaded successfully! ✅")

    # Before cleaning
    st.subheader("🔍 Data Quality Before Cleaning")

    before_report = validate_data(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", before_report["rows"])
    col2.metric("Columns", before_report["columns"])
    col3.metric("Duplicates", before_report["duplicate_rows"])
    col4.metric("Missing Values", before_report["missing_values"])

    # Show raw data
    with st.expander("👀 View Raw Data"):
        st.dataframe(df, use_container_width=True)

    # Clean button
    # Clean button
    if st.button("🧹 Clean & Analyze Data", use_container_width=True):

        import time

        # Animation
        progress_text = st.empty()
        progress_bar = st.progress(0)

        progress_text.info("🔍 Inspecting your dataset...")
        progress_bar.progress(20)
        time.sleep(0.6)

        progress_text.info("🧹 Cleaning duplicate and invalid data...")
        progress_bar.progress(45)
        time.sleep(0.6)

        # Clean data
        cleaned_df = clean_data(df)

        progress_text.info("✅ Validating cleaned data...")
        progress_bar.progress(70)
        time.sleep(0.6)

        # Validate
        after_report = validate_data(cleaned_df)

        progress_text.info("📊 Generating analysis and insights...")
        progress_bar.progress(90)
        time.sleep(0.6)

        progress_bar.progress(100)

        progress_text.success(
            "🎉 Data cleaning and analysis completed!"
        )

        time.sleep(0.5)

        # =========================
        # AFTER CLEANING
        # =========================

        st.subheader("✨ Data Quality After Cleaning")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", after_report["rows"])
        col2.metric("Columns", after_report["columns"])
        col3.metric("Duplicates", after_report["duplicate_rows"])
        col4.metric("Missing Values", after_report["missing_values"])


        # =========================
        # KPIs
        # =========================
        st.subheader("🔄 Before vs After Cleaning")

        before_rows = before_report["rows"]
        after_rows = after_report["rows"]

        before_missing = before_report["missing_values"]
        after_missing = after_report["missing_values"]

        before_duplicates = before_report["duplicate_rows"]
        after_duplicates = after_report["duplicate_rows"]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Rows Removed",
            before_rows - after_rows
        )
        col2.metric(
           "Missing Values Reduced",
           before_missing - after_missing
        )
        col3.metric(
           "Duplicate Rows Removed",
              before_duplicates - after_duplicates
        )
        st.markdown("### 🧹 Cleaning Impact")

        rows_removed = before_rows - after_rows
        missing_reduced = before_missing - after_missing
        duplicates_removed = before_duplicates - after_duplicates

        st.write("**Rows Removed**")
        st.progress(
            min(rows_removed / max(before_rows, 1), 1.0)
        )

        st.write("**Missing Values Reduced**")
        st.progress(
            min(missing_reduced / max(before_missing, 1), 1.0)
            if before_missing > 0 else 1.0
        )
        st.write("**Duplicate Rows Removed**")
        st.progress(
            min(duplicates_removed / max(before_duplicates, 1), 1.0)
            if before_duplicates > 0 else 0.0
        )
            
        st.subheader("📈 Business KPIs")

        kpis = calculate_kpis(cleaned_df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", f"{kpis['Total Rows']:,}")
        col2.metric("Total Columns", f"{kpis['Total Columns']:,}")
        col3.metric("Missing Values", f"{kpis['Missing Values']:,}")
        col4.metric("Duplicate Rows", f"{kpis['Duplicate Rows']:,}")

        st.subheader("💡 Automatic Data Insights")
        insights = generate_insights(cleaned_df)
        for insight in insights:
           st.info(insight)

        # =========================
        # CHARTS
        # =========================

        st.subheader("📊 Automatic Data Visualization")

        numeric_columns = cleaned_df.select_dtypes(
        include="number"
        ).columns.tolist()

        categorical_columns = cleaned_df.select_dtypes(
        include=["object", "string", "category"]
        ).columns.tolist()

        date_columns = []

        for column in cleaned_df.columns:
         converted = pd.to_datetime(
         cleaned_df[column],
        errors="coerce"
        )

        if converted.notna().sum() >= len(cleaned_df) * 0.7:
          date_columns.append(column)


        # Numeric Charts
        if numeric_columns:
         st.markdown("### 🔢 Numeric Data")

        for column in numeric_columns[:4]:
         from modules.visualization import create_numeric_chart

        fig = create_numeric_chart(
            cleaned_df,
            column
        )

        st.pyplot(fig)


        # Categorical Charts
        if categorical_columns:
         st.markdown("### 📊 Categorical Data")

         for column in categorical_columns[:4]:
          from modules.visualization import create_categorical_chart

        fig = create_categorical_chart(
            cleaned_df,
            column
        )

        st.pyplot(fig)


       # Date + Numeric Chart
        if len(date_columns) > 0 and len(numeric_columns) > 0:
  
            st.markdown("### 📅 Trend Analysis")

            from modules.visualization import create_date_chart

            fig = create_date_chart(
               cleaned_df,
               date_columns[0],
               numeric_columns[0]
           )

            st.pyplot(fig)

        
        else:
            st.info("📅 No suitable date column was detected for trend analysis.")


       # Correlation Chart
        if len(numeric_columns) >= 2:

         st.markdown("### 🔗 Correlation Analysis")

        from modules.visualization import create_correlation_chart

        fig = create_correlation_chart(
        cleaned_df
       )

        if fig is not None:
         st.pyplot(fig)


        # =========================
        # CLEANED DATA
        # =========================

        st.subheader("🧹 Cleaned Dataset")

        st.dataframe(
            cleaned_df,
            use_container_width=True
        )

        # st.download_button(
        #    "📥 Download Cleaned CSV",
        #    cleaned_df.to_csv(index=False),
        #    "cleaned_data.csv",
        #    "text/csv",
        #    use_container_width=True
        #)

        # =========================
        # CSV DOWNLOAD
        # =========================

        csv = cleaned_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv",
            use_container_width=True
        )


        # =========================
        # EXCEL REPORT
        # =========================

        report_file = generate_excel_report(
            cleaned_df,
            kpis,
            after_report
        )

        st.subheader("📑 Automated Report")

        with open(report_file, "rb") as file:
            report_data = file.read()

        st.download_button(
            label="📥 Download Automated Excel Report",
            data=report_data,
            file_name="automated_data_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )