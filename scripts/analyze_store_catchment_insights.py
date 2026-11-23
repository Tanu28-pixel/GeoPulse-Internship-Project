import pandas as pd

# Load store performance data
input_file = "data/processed/store_performance_ranking.csv"

df = pd.read_csv(input_file)

# Validate required columns
required_columns = [
    "StoreID",
    "StoreName",
    "StoreType",
    "unique_visitors",
    "Rank"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")

# Compare Existing vs Proposed stores
summary = df.groupby("StoreType")["unique_visitors"].agg(
    Total_Visitors="sum",
    Average_Visitors="mean",
    Highest_Visitors="max",
    Lowest_Visitors="min",
    Store_Count="count"
).reset_index()

print("\n===== EXISTING VS PROPOSED STORE ANALYSIS =====")
print(summary.to_string(index=False))

# Calculate average visitor gap
existing_avg = summary.loc[
    summary["StoreType"] == "Existing", "Average_Visitors"
].iloc[0]

proposed_avg = summary.loc[
    summary["StoreType"] == "Proposed", "Average_Visitors"
].iloc[0]

visitor_gap = proposed_avg - existing_avg

percentage_difference = (visitor_gap / existing_avg) * 100

print("\n===== COMPARISON =====")
print(f"Existing Average Visitors : {existing_avg:.2f}")
print(f"Proposed Average Visitors: {proposed_avg:.2f}")
print(f"Visitor Difference       : {visitor_gap:.2f}")
print(f"Percentage Difference    : {percentage_difference:.2f}%")

# Identify highest and lowest visitor locations
highest_store = df.loc[df["unique_visitors"].idxmax()]
lowest_store = df.loc[df["unique_visitors"].idxmin()]

print("\n===== STORE PERFORMANCE =====")
print(
    f"Highest: {highest_store['StoreName']} | "
    f"{highest_store['unique_visitors']} visitors"
)

print(
    f"Lowest: {lowest_store['StoreName']} | "
    f"{lowest_store['unique_visitors']} visitors"
)

# Generate business interpretation
print("\n===== BUSINESS INSIGHT =====")

if proposed_avg > existing_avg:
    print("Proposed locations have higher average visitor potential.")
elif proposed_avg < existing_avg:
    print("Existing locations have higher average visitor potential.")
else:
    print("Existing and proposed locations have equal average visitor potential.")

# Export summary
output_file = "data/processed/store_catchment_insights.csv"

summary.to_csv(output_file, index=False)

print(f"\nSummary saved to: {output_file}")