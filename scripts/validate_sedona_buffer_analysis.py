import pandas as pd
import glob

# Load store data
stores_df = pd.read_csv("data/raw/store_locations.csv")

# Automatically find the Spark-generated CSV file
files = glob.glob(
    "data/processed/sedona_buffer_analysis/part-*.csv"
)

if not files:
    raise FileNotFoundError("No catchment result CSV found.")

results_df = pd.read_csv(files[0])

print("GEOPULSE BUFFER ANALYSIS VALIDATION")
print("---------------------------------")

print("Expected stores:", len(stores_df))
print("Stores in results:", len(results_df))
print("Unique Store IDs:", results_df["StoreID"].nunique())
print("Duplicate Store IDs:", results_df["StoreID"].duplicated().sum())
print("Negative visitor counts:", (results_df["unique_visitors"] < 0).sum())
print("Stores with zero visitors:", (results_df["unique_visitors"] == 0).sum())
print("Missing values:", results_df.isnull().sum().sum())

missing_stores = set(stores_df["StoreID"]) - set(results_df["StoreID"])
print("Missing stores:", missing_stores)

if (
    len(results_df) == len(stores_df)
    and results_df["StoreID"].is_unique
    and (results_df["unique_visitors"] >= 0).all()
    and results_df.isnull().sum().sum() == 0
    and not missing_stores
):
    print("\nVALIDATION PASSED!")
else:
    print("\nVALIDATION FAILED!")