import pandas as pd

input_file = "data/processed/retail_location_recommendations.csv"

df = pd.read_csv(input_file)

print("\n===== RETAIL LOCATION RECOMMENDATION VALIDATION =====")

# 1. Check total proposed locations
assert len(df) == 10, "Expected exactly 10 proposed locations"
print("Total locations check: PASSED")

# 2. Check duplicate StoreIDs
assert df["StoreID"].is_unique, "Duplicate StoreIDs found"
print("Duplicate StoreID check: PASSED")

# 3. Check missing values
assert not df.isnull().any().any(), "Missing values found"
print("Missing values check: PASSED")

# 4. Check negative visitor counts
assert (df["unique_visitors"] >= 0).all(), "Negative visitor counts found"
print("Visitor count check: PASSED")

# 5. Check recommendation scores
assert df["Recommendation_Score"].between(0, 100).all(), \
    "Scores outside 0-100 range"
print("Score range check: PASSED")

# 6. Validate recommendation categories
def expected_category(visitors):
    if visitors >= 18000:
        return "High Priority"
    elif visitors >= 10000:
        return "Medium Priority"
    elif visitors > 0:
        return "Low Priority"
    else:
        return "No Visitor Potential"

expected = df["unique_visitors"].apply(expected_category)

assert (df["Recommendation"] == expected).all(), \
    "Incorrect recommendation classifications found"

print("Recommendation classification check: PASSED")

# 7. Validate descending score order
assert df["Recommendation_Score"].is_monotonic_decreasing, \
    "Recommendations are not sorted correctly"

print("Sorting check: PASSED")

print("\nALL VALIDATION CHECKS PASSED!")