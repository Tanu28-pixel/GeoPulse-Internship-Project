import pandas as pd

input_file = "data/processed/retail_location_recommendations.csv"

df = pd.read_csv(input_file)

total_locations = len(df)

high = df[df["Recommendation"] == "High Priority"]
medium = df[df["Recommendation"] == "Medium Priority"]
low = df[df["Recommendation"] == "Low Priority"]
no_potential = df[df["Recommendation"] == "No Visitor Potential"]

best_location = df.loc[df["unique_visitors"].idxmax()]
worst_location = df.loc[df["unique_visitors"].idxmin()]

report = f"""
========================================================
        GEOPULSE RETAIL LOCATION RECOMMENDATION REPORT
========================================================

PROJECT: GeoPulse - Retail Mobility Analytics

OBJECTIVE:
Identify and rank potential retail store locations using
simulated GPS mobility data and visitor catchment analysis.

--------------------------------------------------------
1. OVERALL SUMMARY
--------------------------------------------------------

Total Proposed Locations Evaluated: {total_locations}

High Priority Locations: {len(high)}
Medium Priority Locations: {len(medium)}
Low Priority Locations: {len(low)}
No Visitor Potential Locations: {len(no_potential)}

--------------------------------------------------------
2. BEST PERFORMING PROPOSED LOCATION
--------------------------------------------------------

Location: {best_location['StoreName']}
Store ID: {best_location['StoreID']}
Estimated Visitors: {best_location['unique_visitors']}
Recommendation Score: {best_location['Recommendation_Score']} / 100
Category: {best_location['Recommendation']}

--------------------------------------------------------
3. LOWEST PERFORMING PROPOSED LOCATION
--------------------------------------------------------

Location: {worst_location['StoreName']}
Store ID: {worst_location['StoreID']}
Estimated Visitors: {worst_location['unique_visitors']}
Recommendation Score: {worst_location['Recommendation_Score']} / 100
Category: {worst_location['Recommendation']}

--------------------------------------------------------
4. HIGH PRIORITY LOCATIONS
--------------------------------------------------------

{high[['StoreName', 'unique_visitors', 'Recommendation_Score']].to_string(index=False)}

--------------------------------------------------------
5. MEDIUM PRIORITY LOCATIONS
--------------------------------------------------------

{medium[['StoreName', 'unique_visitors', 'Recommendation_Score']].to_string(index=False)}

--------------------------------------------------------
6. LOW PRIORITY LOCATIONS
--------------------------------------------------------

{low[['StoreName', 'unique_visitors', 'Recommendation_Score']].to_string(index=False)}

--------------------------------------------------------
7. LOCATIONS WITH NO VISITOR POTENTIAL
--------------------------------------------------------

{no_potential[['StoreName', 'unique_visitors']].to_string(index=False)}

--------------------------------------------------------
8. BUSINESS RECOMMENDATIONS
--------------------------------------------------------

1. Prioritize high-scoring locations for further feasibility studies.

2. Conduct field visits to validate simulated visitor patterns.

3. Investigate locations with zero visitor potential to determine
   whether they have accessibility, data coverage, or location issues.

4. Evaluate rent, competition, customer demographics, visibility,
   and operational costs before making final investment decisions.

5. Use this analysis as a location-screening tool rather than
   the sole basis for opening a retail store.

--------------------------------------------------------
9. METHODOLOGY & LIMITATIONS
--------------------------------------------------------

Recommendations are based on simulated GPS mobility data and
500-meter store catchment analysis.

Visitor counts represent simulated catchment potential and
should not be interpreted as actual retail footfall.

Recommendation scores are relative visitor-potential scores,
not probabilities of business success.

========================================================
                    END OF REPORT
========================================================
"""

output_file = "data/processed/retail_location_recommendation_report.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(report)

print(report)

print(f"\nReport saved to: {output_file}")