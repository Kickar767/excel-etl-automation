import pandas as pd


def clean_sales_dataset(input_csv: str, output_excel: str) -> pd.DataFrame:
    """Clean raw sales records, normalize dates and amounts, and export summary."""
    df = pd.read_csv(input_csv)

    # Remove exact duplicates and empty rows
    df = df.drop_duplicates().dropna(how="all")

    # Normalize text fields and numeric values
    if "category" in df.columns:
        df["category"] = df["category"].astype(str).str.strip().str.title()

    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Build category summary
    summary = (
        df.groupby("category", dropna=False)["amount"]
        .agg(["count", "sum", "mean"])
        .reset_index()
        if "category" in df.columns and "amount" in df.columns
        else pd.DataFrame()
    )

    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned_Data", index=False)
        if not summary.empty:
            summary.to_excel(writer, sheet_name="Summary_By_Category", index=False)

    return df


if __name__ == "__main__":
    print("ETL script ready: clean_sales_dataset(input_csv, output_excel)")
