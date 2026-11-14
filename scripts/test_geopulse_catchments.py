
import duckdb
import pandas as pd

# Step 1: Load GPS dataset (10,000 sample records)
gps_df = pd.read_csv(
    "data/raw/gps_mobility_pings.csv"
)

# Step 2: Load store locations
stores_df = pd.read_csv(
    "data/raw/store_locations.csv"
)

print("GPS Dataset Columns:", gps_df.columns.tolist())
print("Store Dataset Columns:", stores_df.columns.tolist())

# Step 3: Connect to GeoPulse database
con = duckdb.connect("geopulse.duckdb")

# Step 4: Enable spatial extension
con.execute("LOAD spatial")
con.execute("SET geometry_always_xy = true")

# Step 5: Register datasets
con.register("gps_data", gps_df)
con.register("store_data", stores_df)

# Step 6: Find unique visitors within 500 metres
query = """
SELECT
    s.StoreID,
    s.StoreName,
    COUNT(DISTINCT g.DeviceID) AS unique_visitors
FROM gps_data g
CROSS JOIN store_data s
WHERE ST_Distance_Sphere(
    ST_Point(g.Longitude, g.Latitude),
    ST_Point(s.Longitude, s.Latitude)
) <= 500
GROUP BY s.StoreID, s.StoreName
ORDER BY unique_visitors DESC;
"""

# Step 7: Execute analysis
result = con.execute(query).fetchdf()
import os

os.makedirs("data/processed", exist_ok=True)

result.to_csv(
    "data/processed/catchment_analysis.csv",
    index=False
)

print("Catchment results saved successfully!")

print("\nGeoPulse Actual Dataset Catchment Analysis")
print("GPS records tested:", len(gps_df))
print("Stores analysed:", len(stores_df))
print("\nUnique visitors within 500 metres:")
print(result)

con.close()
