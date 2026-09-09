import pandas as pd


def generate_excel_report(cleaned_df, kpis, validation_report):

    output_file = "reports/automated_data_report.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

        # KPI Summary
        kpi_df = pd.DataFrame(
            list(kpis.items()),
            columns=["Metric", "Value"]
        )

        kpi_df.to_excel(
            writer,
            sheet_name="KPI Summary",
            index=False
        )

        # Data Quality
        validation_df = pd.DataFrame(
            list(validation_report.items()),
            columns=["Metric", "Value"]
        )

        validation_df.to_excel(
            writer,
            sheet_name="Data Quality",
            index=False
        )

        # Numeric Summary
        numeric_columns = cleaned_df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) > 0:
            numeric_summary = cleaned_df[numeric_columns].describe().T

            numeric_summary.to_excel(
                writer,
                sheet_name="Numeric Summary"
            )

        # Column Analysis
        column_report = []

        for column in cleaned_df.columns:
            column_report.append({
                "Column": column,
                "Data Type": str(cleaned_df[column].dtype),
                "Missing Values": int(cleaned_df[column].isna().sum()),
                "Unique Values": int(cleaned_df[column].nunique())
            })

        column_df = pd.DataFrame(column_report)
        column_df.to_excel(
            writer,
            sheet_name="Column Analysis",
            index=False
        )


        # Cleaned Dataset
        cleaned_df.to_excel(
            writer,
            sheet_name="Cleaned Data",
            index=False
        )

    return output_file
