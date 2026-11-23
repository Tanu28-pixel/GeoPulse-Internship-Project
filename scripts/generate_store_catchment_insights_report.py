import pandas as pd

# Load analysis results
comparison_file = "data/processed/proposed_store_comparison.csv"
df = pd.read_csv(comparison_file)

# Identify strong and weak proposed locations
strong_locations = df[df["Performance"] == "Above Existing Average"]
weak_locations = df[df["Performance"] == "Below Existing Average"]

# Sort locations by visitor potential
strong_locations = strong_locations.sort_values(
    by="unique_visitors", ascending=False
)

weak_locations = weak_locations.sort_values(
    by="unique_visitors", ascending=True
)

# Generate report
report = []

report.append("=" * 60)
report.append("GEOPULSE - RETAIL CATCHMENT INSIGHTS REPORT")
report.append("=" * 60)

report.append("\nEXISTING STORE BENCHMARK")
report.append(
    f"Existing Store Average Visitors: 14772.50"
)

report.append("\nSTRONG PROPOSED LOCATIONS")
for _, row in strong_locations.iterrows():
    report.append(
        f"{row['StoreName']} | "
        f"Visitors: {row['unique_visitors']} | "
        f"Difference: {row['Percentage_Difference']:.2f}%"
    )

report.append("\nWEAK PROPOSED LOCATIONS")
for _, row in weak_locations.iterrows():
    report.append(
        f"{row['StoreName']} | "
        f"Visitors: {row['unique_visitors']} | "
        f"Difference: {row['Percentage_Difference']:.2f}%"
    )

report.append("\nBUSINESS RECOMMENDATIONS")

report.append(
    "1. Prioritize high-potential proposed locations for further feasibility analysis."
)

report.append(
    "2. Investigate locations with zero visitors to verify spatial data and catchment coverage."
)

report.append(
    "3. Evaluate low-performing locations before making investment decisions."
)

report.append(
    "4. Consider rental costs, competition, accessibility, and demographic factors before final selection."
)

report.append("\nDISCLAIMER")
report.append(
    "Visitor counts represent simulated GPS-based catchment analysis "
    "and should not be treated as actual retail footfall."
)

# Save report
output_file = "data/processed/store_catchment_insights_report.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(report))

# Print report
print("\n".join(report))

print(f"\nReport saved to: {output_file}")