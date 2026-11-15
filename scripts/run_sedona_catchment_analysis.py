
from sedona.spark import SedonaContext

# Start Spark with Apache Sedona
spark = (
    SedonaContext.builder()
    .appName("GeoPulse 500 Meter Catchment Analysis")
    .master("local[*]")
    .config(
    "spark.jars.packages",
    "org.apache.sedona:sedona-spark-shaded-4.1_2.13:1.9.1"
)
.config("sedona.global.index", "false")
.config("sedona.join.autoBroadcastJoinThreshold", "-1")
.config("spark.sql.autoBroadcastJoinThreshold", "-1")
    .getOrCreate()
)

sedona = SedonaContext.create(spark)

# Load GPS mobility data
gps_df = (
    sedona.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/gps_mobility_pings.csv")
)

# Load store locations
stores_df = (
    sedona.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/store_locations.csv")
)

# Create temporary SQL views
gps_df.createOrReplaceTempView("gps_data")
stores_df.createOrReplaceTempView("store_data")

print("Running GeoPulse 500-Meter Spatial Analysis...")

# Find unique devices within 500 metres of each store
query = """
SELECT
    s.StoreID,
    s.StoreName,
    s.StoreType,
    COUNT(DISTINCT g.DeviceID) AS unique_visitors
FROM store_data s
LEFT JOIN gps_data g
    ON ST_DistanceSphere(
        ST_Point(g.Longitude, g.Latitude),
        ST_Point(s.Longitude, s.Latitude)
    ) <= 500
GROUP BY
    s.StoreID,
    s.StoreName,
    s.StoreType
ORDER BY unique_visitors DESC
"""

result = sedona.sql(query)

# Display results
print("\nGEOPULSE CATCHMENT ANALYSIS RESULTS")
result.show(25, truncate=False)

# Save results
result.write.mode("overwrite").option("header", True).csv(
    "data/processed/sedona_catchment_analysis"
)

print("\nAnalysis completed successfully.")
print("Results saved in data/processed/sedona_catchment_analysis/")

sedona.stop()
