import pandas as pd

# Load opportunity analysis results
df = pd.read_csv("data/processed/store_location_opportunities.csv")

print("GEOPULSE LOCATION OPPORTUNITY VALIDATION")
print("-------------------------------------")

print("Total proposed stores:", len(df))
print("Unique Store IDs:", df["StoreID"].nunique())
print("Duplicate Store IDs:", df["StoreID"].duplicated().sum())
print("Missing values:", df.isnull().sum().sum())
print("Negative visitors:", (df["unique_visitors"] < 0).sum())

# Check category validity
valid_categories = [
    "High Opportunity",
    "Medium Opportunity",
    "Low Opportunity",
    "No Visitor Potential"
]

category_valid = df["Opportunity_Category"].isin(
    valid_categories
).all()

# Verify visitor classification
classification_correct = True

for _, row in df.iterrows():
    visitors = row["unique_visitors"]
    category = row["Opportunity_Category"]

    if visitors >= 18000 and category != "High Opportunity":
        classification_correct = False

    elif 10000 <= visitors < 18000 and category != "Medium Opportunity":
        classification_correct = False

    elif 0 < visitors < 10000 and category != "Low Opportunity":
        classification_correct = False

    elif visitors == 0 and category != "No Visitor Potential":
        classification_correct = False

print("Categories valid:", category_valid)
print("Visitor classification correct:", classification_correct)

if (
    len(df) == 10
    and df["StoreID"].is_unique
    and (df["unique_visitors"] >= 0).all()
    and df.isnull().sum().sum() == 0
    and category_valid
    and classification_correct
):
    print("\nVALIDATION PASSED!")
else:
    print("\nVALIDATION FAILED!")