import pandas as pd

# Load Day 6 catchment analysis results
results_df = pd.read_csv(
    "data/processed/sedona_buffer_analysis/"
    "part-00000-79908181-0a75-4830-a6f9-906c89ef0e8e-c000.csv"
)

print("GEOPULSE STORE CATCHMENT PERFORMANCE ANALYSIS")
print("------------------------------------------")

# Store category summary
category_summary = (
    results_df.groupby("StoreType")["unique_visitors"]
    .agg(["count", "mean", "sum", "max", "min"])
    .reset_index()
)

print("\nSTORE CATEGORY PERFORMANCE")
print(category_summary)

# Rank stores based on unique visitors
store_ranking = results_df.sort_values(
    by="unique_visitors",
    ascending=False
).reset_index(drop=True)

store_ranking["Rank"] = store_ranking.index + 1

print("\nSTORE PERFORMANCE RANKING")
print(
    store_ranking[
        ["Rank", "StoreID", "StoreName", "StoreType", "unique_visitors"]
    ].to_string(index=False)
)

# Identify the best proposed store locations
proposed_stores = store_ranking[
    store_ranking["StoreType"] == "Proposed"
]

print("\nTOP PROPOSED STORE LOCATIONS")
print(
    proposed_stores[
        ["Rank", "StoreName", "unique_visitors"]
    ].to_string(index=False)
)

# Save results
category_summary.to_csv(
    "data/processed/store_category_performance.csv",
    index=False
)

store_ranking.to_csv(
    "data/processed/store_performance_ranking.csv",
    index=False
)

print("\nAnalysis completed successfully!")
print("Results saved in data/processed/")
# Business Insights
print("\nGEOPULSE BUSINESS INSIGHTS")
print("------------------------")

existing_avg = results_df[
    results_df["StoreType"] == "Existing"
]["unique_visitors"].mean()

proposed_avg = results_df[
    results_df["StoreType"] == "Proposed"
]["unique_visitors"].mean()

difference = proposed_avg - existing_avg
percentage_difference = (difference / existing_avg) * 100

print(f"Average existing store visitors: {existing_avg:.2f}")
print(f"Average proposed store visitors: {proposed_avg:.2f}")
print(f"Visitor difference: {difference:.2f}")
print(f"Percentage difference: {percentage_difference:.2f}%")

top_store = results_df.loc[
    results_df["unique_visitors"].idxmax()
]

print(
    f"\nHighest-performing location: {top_store['StoreName']}"
    f" ({top_store['unique_visitors']} visitors)"
)

zero_visitor_stores = results_df[
    results_df["unique_visitors"] == 0
]

print("Stores with zero visitors:", len(zero_visitor_stores))
