import pandas as pd

# Load store catchment performance results
df = pd.read_csv("data/processed/store_performance_ranking.csv")

# Filter proposed store locations
proposed_df = df[df["StoreType"] == "Proposed"].copy()

# Sort by visitor potential
proposed_df = proposed_df.sort_values(
    by="unique_visitors",
    ascending=False
).reset_index(drop=True)

# Assign opportunity categories
def classify_location(visitors):
    if visitors >= 18000:
        return "High Opportunity"
    elif visitors >= 10000:
        return "Medium Opportunity"
    elif visitors > 0:
        return "Low Opportunity"
    else:
        return "No Visitor Potential"

proposed_df["Opportunity_Category"] = proposed_df[
    "unique_visitors"
].apply(classify_location)

print("GEOPULSE STORE LOCATION OPPORTUNITY ANALYSIS")
print("------------------------------------------")

print(
    proposed_df[
        ["StoreName", "unique_visitors", "Opportunity_Category"]
    ].to_string(index=False)
)

# Category summary
category_summary = (
    proposed_df.groupby("Opportunity_Category")
    .agg(
        store_count=("StoreID", "count"),
        average_visitors=("unique_visitors", "mean"),
        total_visitors=("unique_visitors", "sum")
    )
    .reset_index()
)

print("\nOPPORTUNITY CATEGORY SUMMARY")
print(category_summary.to_string(index=False))

# Save outputs
proposed_df.to_csv(
    "data/processed/store_location_opportunities.csv",
    index=False
)

category_summary.to_csv(
    "data/processed/opportunity_category_summary.csv",
    index=False
)

print("\nOpportunity analysis completed successfully!")
print("Results saved in data/processed/")