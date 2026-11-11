
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "raw" / "gps_mobility_pings.csv"

def validate_gps_data():

    print("Starting GPS Data Quality Validation...\n")

    if not INPUT_FILE.exists():
        print("ERROR: GPS dataset not found!")
        return

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "DeviceID",
        "Latitude",
        "Longitude",
        "Timestamp"
    ]

    # Column validation
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    print("Total Records:", len(df))
    print("Unique Devices:", df["DeviceID"].nunique())

    # Missing value validation
    print("\nMissing Values:")
    print(df[required_columns].isnull().sum())

    # Duplicate validation
    print("\nDuplicate Rows:", df.duplicated().sum())

    # Coordinate validation
    invalid_latitudes = (
        ~df["Latitude"].between(-90, 90)
    ).sum()

    invalid_longitudes = (
        ~df["Longitude"].between(-180, 180)
    ).sum()

    print("\nInvalid Latitudes:", invalid_latitudes)
    print("Invalid Longitudes:", invalid_longitudes)

    # Timestamp validation
    timestamps = pd.to_datetime(
        df["Timestamp"], errors="coerce"
    )

    print("Invalid Timestamps:", timestamps.isna().sum())

    # Geographic range
    print("\nLatitude Range:",
          df["Latitude"].min(),
          df["Latitude"].max())

    print("Longitude Range:",
          df["Longitude"].min(),
          df["Longitude"].max())

    # Final status
    passed = (
        df[required_columns].notnull().all().all()
        and df.duplicated().sum() == 0
        and invalid_latitudes == 0
        and invalid_longitudes == 0
        and timestamps.notna().all()
    )

    print("\n" + "=" * 45)

    if passed:
        print("RESULT: GPS DATA VALIDATION PASSED")
    else:
        print("RESULT: GPS DATA VALIDATION FAILED")

    print("=" * 45)


if __name__ == "__main__":
    validate_gps_data()
