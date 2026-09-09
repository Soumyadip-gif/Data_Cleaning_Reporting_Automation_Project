import pandas as pd


def validate_data(df):
    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum()),
        "negative_quantity": 0,
        "negative_sales": 0,
        "invalid_dates": 0
    }

    if "Quantity" in df.columns:
        report["negative_quantity"] = int(
            (pd.to_numeric(df["Quantity"], errors="coerce") < 0).sum()
        )

    if "Sales" in df.columns:
        report["negative_sales"] = int(
            (pd.to_numeric(df["Sales"], errors="coerce") < 0).sum()
        )

    if "Date" in df.columns:
        dates = pd.to_datetime(df["Date"], errors="coerce")
        report["invalid_dates"] = int(dates.isna().sum())

    return report
