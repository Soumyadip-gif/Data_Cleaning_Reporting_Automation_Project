import pandas as pd


def clean_data(df):
    df = df.copy()

    # 1. Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
    )

    # 2. Remove completely empty rows and columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # 3. Remove duplicate rows
    df = df.drop_duplicates()

    # 4. Clean text columns
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        # Convert empty strings to missing values
        df[column] = df[column].replace("", pd.NA)

    # 5. Detect and clean date columns
    date_keywords = [
        "date",
        "time",
        "dob",
        "birth",
        "created",
        "updated",
        "joined"
    ]

    for column in df.columns:

        column_name = column.lower()

        if any(keyword in column_name for keyword in date_keywords):

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            # Convert only if at least one valid date exists
            if converted.notna().sum() > 0:
                df[column] = converted.dt.strftime("%Y-%m-%d")

    # 6. Detect numeric columns
    for column in df.columns:

        if df[column].dtype in ["object", "string"]:

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            non_empty = df[column].notna().sum()

            if non_empty > 0:

                numeric_ratio = (
                    converted.notna().sum() / non_empty
                )

                # If 80% or more values are numeric
                if numeric_ratio >= 0.8:
                    df[column] = converted

    # 7. Fill missing numeric values
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        df[column] = df[column].fillna(
            df[column].median()
        )

    return df