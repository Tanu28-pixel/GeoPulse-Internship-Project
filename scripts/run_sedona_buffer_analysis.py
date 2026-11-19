from sedona.spark import SedonaContext

# Start Spark with Apache Sedona
spark = (
    SedonaContext.builder()
    .appName("GeoPulse Store Buffer Analysis")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-shaded-4.1_2.13:1.9.1"
    )
    .getOrCreate()
)

sedona = SedonaContext.create(spark)

# Load GPS data
gps_df = (
    sedona.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/gps_mobility_pings.csv")
)

# Load store data
stores_df = (
    sedona.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/store_locations.csv")
)

gps_df.createOrReplaceTempView("gps_data")
stores_df.createOrReplaceTempView("store_data")

print("Creating 500-Meter Catchment Polygons...")

query = """
WITH store_buffers AS (
    SELECT
        StoreID,
        StoreName,
        StoreType,
        ST_Buffer(
            ST_Transform(
                ST_SetSRID(ST_Point(Longitude, Latitude), 4326),
                'EPSG:4326',
                'EPSG:32643'
            ),
            500
        ) AS catchment_polygon
    FROM store_data
),
gps_points AS (
    SELECT
        DeviceID,
        ST_Transform(
            ST_SetSRID(ST_Point(Longitude, Latitude), 4326),
            'EPSG:4326',
            'EPSG:32643'
        ) AS gps_point
    FROM gps_data
)
SELECT
    s.StoreID,
    s.StoreName,
    s.StoreType,
    COUNT(DISTINCT g.DeviceID) AS unique_visitors
FROM store_buffers s
LEFT JOIN gps_points g
    ON ST_Contains(s.catchment_polygon, g.gps_point)
GROUP BY
    s.StoreID,
    s.StoreName,
    s.StoreType
ORDER BY unique_visitors DESC
"""

result = sedona.sql(query)

print("\nGEOPULSE 500-METER POLYGON ANALYSIS")
result.show(20, truncate=False)

# Save results
result.write.mode("overwrite").option("header", True).csv(
    "data/processed/sedona_buffer_analysis"
)

print("\nPolygon-based catchment analysis completed.")
print("Results saved in data/processed/sedona_buffer_analysis/")

sedona.stop()