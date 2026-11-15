
from sedona.spark import SedonaContext

spark = (
    SedonaContext.builder()
    .appName("GeoPulse Sedona Distance Test")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-shaded-4.1_2.13:1.9.1"
    )
    .getOrCreate()
)

sedona = SedonaContext.create(spark)

result = sedona.sql("""
    SELECT
        ST_DistanceSphere(
            ST_Point(77.6068, 12.9756),
            ST_Point(77.6010, 12.9719)
        ) AS distance_meters
""")

print("GEOPULSE SEDONA DISTANCE TEST")
result.show(truncate=False)

sedona.stop()
