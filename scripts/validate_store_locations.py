
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "raw" / "store_locations.csv"


def validate_store_locations():

    print("Starting Store Location Data Validation...\n")

    if not INPUT_FILE.exists():
        print("ERROR: Store location dataset not found!")
        return

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "StoreID",
        "StoreName",
        "Latitude",
        "Longitude",
        "StoreType"
    ]

    # Check required columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("Missing Columns:", missing_columns)
        return

    # Basic record statistics
    print("Total Stores:", len(df))
    print("Unique Store IDs:", df["StoreID"].nunique())

    # Missing values
    print("\nMissing Values:")
    print(df[required_columns].isnull().sum())

    # Duplicate validation
    print("\nDuplicate Rows:", df.duplicated().sum())
    print("Duplicate Store IDs:", df["StoreID"].duplicated().sum())

    # Coordinate validation
    df["Latitude"] = pd.to_numeric(
        df["Latitude"], errors="coerce"
    )
    df["Longitude"] = pd.to_numeric(
        df["Longitude"], errors="coerce"
    )

    invalid_latitudes = (
        ~df["Latitude"].between(-90, 90)
    ).sum()

    invalid_longitudes = (
        ~df["Longitude"].between(-180, 180)
    ).sum()

    print("\nInvalid Latitudes:", invalid_latitudes)
    print("Invalid Longitudes:", invalid_longitudes)

    # Store category counts
    print("\nStore Types:")
    print(df["StoreType"].value_counts())

    # Coordinate ranges
    print("\nLatitude Range:",
          df["Latitude"].min(),
          df["Latitude"].max())

    print("Longitude Range:",
          df["Longitude"].min(),
          df["Longitude"].max())

    # Final validation
    passed = (
        df[required_columns].notnull().all().all()
        and df["StoreID"].is_unique
        and df["StoreName"].is_unique
        and df.duplicated().sum() == 0
        and invalid_latitudes == 0
        and invalid_longitudes == 0
        and df["StoreType"].isin(["Existing", "Proposed"]).all()
    )

    print("\n" + "=" * 45)

    if passed:
        print("RESULT: STORE LOCATION VALIDATION PASSED")
    else:
        print("RESULT: STORE LOCATION VALIDATION FAILED")

    print("=" * 45)


if __name__ == "__main__":
    validate_store_locations()
