
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("GeoPulse GPS Data Loading")
    .master("local[*]")
    .getOrCreate()
)

# Read GPS mobility data
gps_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/gps_mobility_pings.csv")
)

# Read store location data
stores_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/store_locations.csv")
)

print("GEOPULSE DATA LOADING REPORT")
print("----------------------------")

print("GPS Records:", gps_df.count())
print("Store Records:", stores_df.count())

print("\nGPS Schema:")
gps_df.printSchema()

print("\nStore Schema:")
stores_df.printSchema()

print("\nGPS Sample:")
gps_df.show(5, truncate=False)

print("\nStore Sample:")
stores_df.show(5, truncate=False)

spark.stop()
