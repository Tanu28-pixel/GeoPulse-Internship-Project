
import pandas as pd

# Load the GPS sample and store locations
gps_df = pd.read_csv(
    "data/raw/gps_mobility_pings.csv"
)

stores_df = pd.read_csv(
    "data/raw/store_locations.csv"
)

# Load catchment analysis results
# First, save your query output as a CSV in the next step.
results_df = pd.read_csv(
    "data/processed/catchment_analysis.csv"
)

print("GEOPULSE CATCHMENT DATA VALIDATION")
print("----------------------------------")

print("GPS records tested:", len(gps_df))
print("Unique devices in GPS sample:", gps_df["DeviceID"].nunique())
print("Total stores:", len(stores_df))
print("Stores with catchment results:", results_df["StoreID"].nunique())

print("Negative visitor counts:",
      (results_df["unique_visitors"] < 0).sum())

print("Duplicate store IDs in results:",
      results_df["StoreID"].duplicated().sum())

missing_stores = set(stores_df["StoreID"]) - set(results_df["StoreID"])

print("Stores without results:", missing_stores)

if (
    (results_df["unique_visitors"] >= 0).all()
    and results_df["StoreID"].is_unique
):
    print("\nBasic catchment validation passed!")
else:
    print("\nValidation failed. Please inspect the results.")
