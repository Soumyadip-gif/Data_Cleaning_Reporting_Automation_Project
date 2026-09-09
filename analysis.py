import pandas as pd


def calculate_kpis(df):
    numeric_columns = df.select_dtypes(include="number").columns

    total_rows = len(df)
    total_columns = len(df.columns)
    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    if len(numeric_columns) > 0:
        numeric_total = df[numeric_columns].sum().sum()
        numeric_average = df[numeric_columns].mean().mean()
    else:
        numeric_total = 0
        numeric_average = 0

    return {
        "Total Rows": total_rows,
        "Total Columns": total_columns,
        "Missing Values": missing_values,
        "Duplicate Rows": duplicate_rows,
        "Numeric Total": numeric_total,
        "Numeric Average": numeric_average
    }


def numeric_summary(df):
    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) == 0:
        return pd.DataFrame()

    return df[numeric_columns].describe().T


def categorical_summary(df):
    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    if len(categorical_columns) == 0:
        return pd.DataFrame()

    result = {}

    for column in categorical_columns:
        result[column] = {
            "Unique Values": df[column].nunique(),
            "Missing Values": df[column].isna().sum()
        }

    return pd.DataFrame(result).T


def column_analysis(df):
    analysis = []

    for column in df.columns:
        analysis.append({
            "Column": column,
            "Data Type": str(df[column].dtype),
            "Missing Values": int(df[column].isna().sum()),
            "Unique Values": int(df[column].nunique()),
            "Duplicate Values": int(df[column].duplicated().sum())
        })

    return pd.DataFrame(analysis)

def generate_insights(df):
    insights = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    # Numeric insights
    for column in numeric_columns[:5]:
        if df[column].notna().sum() > 0:
            max_value = df[column].max()
            min_value = df[column].min()
            avg_value = df[column].mean()

            insights.append(
                f"📈 {column}: Average = {avg_value:.2f}, "
                f"Maximum = {max_value}, Minimum = {min_value}"
            )

    # Categorical insights
    for column in categorical_columns[:5]:
        if df[column].notna().sum() > 0:
            top_value = df[column].mode().iloc[0]

            insights.append(
                f"🏆 {column}: Most common value is '{top_value}'"
            )

    # Missing-value insight
    missing_values = int(df.isna().sum().sum())

    if missing_values == 0:
        insights.append("✅ No missing values found in the cleaned dataset.")
    else:
        insights.append(
            f"⚠️ The cleaned dataset still contains "
            f"{missing_values} missing values."
        )

    # Dataset size insight
    insights.append(
         f"📊 Dataset contains {len(df):,} rows "
         f"and {len(df.columns):,} columns after cleaning."
    )
         
           
    return insights