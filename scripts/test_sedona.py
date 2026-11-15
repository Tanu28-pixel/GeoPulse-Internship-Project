
from sedona.spark import SedonaContext

config = (
    SedonaContext.builder()
    .appName("GeoPulse Sedona Test")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-shaded-4.1_2.13:1.9.1"
    )
    .getOrCreate()
)

sedona = SedonaContext.create(config)

print("GeoPulse Apache Sedona Started!")
print("Spark Version:", sedona.version)

result = sedona.sql("""
    SELECT ST_AsText(ST_Point(77.5946, 12.9716)) AS location
""")

result.show(truncate=False)

sedona.stop()
