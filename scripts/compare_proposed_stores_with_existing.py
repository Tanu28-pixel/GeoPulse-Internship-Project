import pandas as pd

# Load store performance data
input_file = "data/processed/store_performance_ranking.csv"
df = pd.read_csv(input_file)

# Separate existing and proposed stores
existing_stores = df[df["StoreType"] == "Existing"]
proposed_stores = df[df["StoreType"] == "Proposed"].copy()

# Calculate existing store benchmark
existing_avg = existing_stores["unique_visitors"].mean()

# Compare proposed locations against existing store benchmark
proposed_stores["Visitor_Gap"] = (
    proposed_stores["unique_visitors"] - existing_avg
)

proposed_stores["Percentage_Difference"] = (
    proposed_stores["Visitor_Gap"] / existing_avg
) * 100

# Classify proposed locations
proposed_stores["Performance"] = proposed_stores[
    "Visitor_Gap"
].apply(
    lambda x: "Above Existing Average"
    if x >= 0
    else "Below Existing Average"
)

# Sort by visitor potential
proposed_stores = proposed_stores.sort_values(
    by="unique_visitors",
    ascending=False
)

# Display results
print("\n===== PROPOSED STORE COMPARISON =====")
print(f"Existing Store Benchmark: {existing_avg:.2f} visitors")

print(
    proposed_stores[
        [
            "StoreID",
            "StoreName",
            "unique_visitors",
            "Visitor_Gap",
            "Percentage_Difference",
            "Performance"
        ]
    ].to_string(index=False)
)

# Export results
output_file = "data/processed/proposed_store_comparison.csv"

proposed_stores.to_csv(output_file, index=False)

print(f"\nComparison report saved to: {output_file}")