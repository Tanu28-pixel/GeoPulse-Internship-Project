import pandas as pd

# Load store performance ranking
results_df = pd.read_csv(
    "data/processed/store_performance_ranking.csv"
)

# Load original store locations
stores_df = pd.read_csv("data/raw/store_locations.csv")

print("GEOPULSE STORE PERFORMANCE VALIDATION")
print("----------------------------------")

print("Total stores:", len(results_df))
print("Unique Store IDs:", results_df["StoreID"].nunique())
print("Duplicate Store IDs:", results_df["StoreID"].duplicated().sum())
print("Missing values:", results_df.isnull().sum().sum())
print("Negative visitors:", (results_df["unique_visitors"] < 0).sum())
print("Unique ranks:", results_df["Rank"].nunique())

# Check ranking order
ranking_correct = results_df["unique_visitors"].is_monotonic_decreasing

# Check rank sequence
rank_sequence_correct = (
    results_df["Rank"].tolist() == list(range(1, len(results_df) + 1))
)

# Check store classification
classification_correct = (
    results_df["StoreType"].isin(["Existing", "Proposed"]).all()
)

# Check missing stores
missing_stores = set(stores_df["StoreID"]) - set(results_df["StoreID"])

print("Ranking sorted correctly:", ranking_correct)
print("Rank sequence correct:", rank_sequence_correct)
print("Store classification valid:", classification_correct)
print("Missing stores:", missing_stores)

if (
    len(results_df) == len(stores_df)
    and results_df["StoreID"].is_unique
    and results_df["unique_visitors"].ge(0).all()
    and results_df.isnull().sum().sum() == 0
    and results_df["Rank"].is_unique
    and ranking_correct
    and rank_sequence_correct
    and classification_correct
    and not missing_stores
):
    print("\nVALIDATION PASSED!")
else:
    print("\nVALIDATION FAILED!")