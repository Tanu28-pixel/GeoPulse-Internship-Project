from sedona.spark import SedonaContext

spark = (
    SedonaContext.builder()
    .appName("GeoPulse 500m Buffer Test")
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
        ST_Area(
            ST_Buffer(
                ST_Transform(
                    ST_SetSRID(ST_Point(77.6068, 12.9756), 4326),
                    'EPSG:4326',
                    'EPSG:32643'
                ),
                500
            )
        ) AS buffer_area_sq_meters
""")

print("GEOPULSE 500-METER BUFFER TEST")
result.show(truncate=False)

sedona.stop()