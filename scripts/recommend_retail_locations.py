import pandas as pd

# Load proposed store performance data
input_file = "data/processed/store_performance_ranking.csv"

df = pd.read_csv(input_file)

# Filter proposed locations
proposed = df[df["StoreType"] == "Proposed"].copy()

# Assign recommendation categories
def classify_location(visitors):
    if visitors >= 18000:
        return "High Priority"
    elif visitors >= 10000:
        return "Medium Priority"
    elif visitors > 0:
        return "Low Priority"
    else:
        return "No Visitor Potential"

# Apply classification
proposed["Recommendation"] = proposed["unique_visitors"].apply(
    classify_location
)

# Assign recommendation scores
def calculate_score(visitors):
    return round((visitors / 20000) * 100, 2)

proposed["Recommendation_Score"] = proposed["unique_visitors"].apply(
    calculate_score
)

# Sort locations by recommendation score
proposed = proposed.sort_values(
    by="Recommendation_Score",
    ascending=False
)

# Display recommendations
print("\n===== GEOPULSE RETAIL LOCATION RECOMMENDATIONS =====")

print(
    proposed[
        [
            "StoreID",
            "StoreName",
            "unique_visitors",
            "Recommendation_Score",
            "Recommendation"
        ]
    ].to_string(index=False)
)

# Export recommendations
output_file = "data/processed/retail_location_recommendations.csv"

proposed.to_csv(output_file, index=False)

print(f"\nRecommendations saved to: {output_file}")