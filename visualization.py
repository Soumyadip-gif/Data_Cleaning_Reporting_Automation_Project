import matplotlib.pyplot as plt
import pandas as pd


def create_numeric_chart(df, column):
    fig, ax = plt.subplots(figsize=(8, 5))

    df[column].dropna().plot(
        kind="hist",
        ax=ax,
        bins=20
    )

    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    plt.tight_layout()

    return fig


def create_categorical_chart(df, column):
    counts = df[column].dropna().value_counts().head(10)

    fig, ax = plt.subplots(figsize=(8, 5))

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(f"Top Values in {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


def create_date_chart(df, date_column, numeric_column):
    temp_df = df.copy()

    temp_df[date_column] = pd.to_datetime(
        temp_df[date_column],
        errors="coerce"
    )

    temp_df = temp_df.dropna(
        subset=[date_column, numeric_column]
    )

    grouped = (
        temp_df
        .groupby(date_column)[numeric_column]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    grouped.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_title(
        f"{numeric_column} Trend Over Time"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel(numeric_column)

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


def create_correlation_chart(df):
    numeric_df = df.select_dtypes(
        include="number"
    )

    if numeric_df.shape[1] < 2:
        return None

    correlation = numeric_df.corr()

    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    image = ax.imshow(
        correlation,
        aspect="auto"
    )

    ax.set_xticks(
        range(len(correlation.columns))
    )
    ax.set_yticks(
        range(len(correlation.columns))
    )

    ax.set_xticklabels(
        correlation.columns,
        rotation=45,
        ha="right"
    )

    ax.set_yticklabels(
        correlation.columns
    )

    ax.set_title(
        "Correlation Between Numeric Columns"
    )

    fig.colorbar(
        image,
        ax=ax
    )

    plt.tight_layout()

    return fig