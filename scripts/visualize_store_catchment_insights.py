import pandas as pd
import matplotlib.pyplot as plt

# Load store performance data
input_file = "data/processed/store_performance_ranking.csv"
df = pd.read_csv(input_file)

# Calculate average visitors by store type
comparison = df.groupby("StoreType")["unique_visitors"].mean()

# Create visualization
plt.figure(figsize=(8, 5))

plt.bar(
    comparison.index,
    comparison.values,
    width=0.5
)

plt.title("Existing vs Proposed Store Catchment Performance")
plt.xlabel("Store Category")
plt.ylabel("Average Unique Visitors")
plt.grid(axis="y", linestyle="--", alpha=0.4)

# Add values on top of bars
for i, value in enumerate(comparison.values):
    plt.text(i, value + 200, f"{value:,.0f}", ha="center")

plt.tight_layout()

# Save chart
output_file = "data/processed/store_catchment_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

plt.show()

print(f"Chart saved to: {output_file}")