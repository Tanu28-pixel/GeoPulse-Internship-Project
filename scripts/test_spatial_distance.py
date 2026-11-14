
import duckdb

con = duckdb.connect("geopulse.duckdb")

con.execute("LOAD spatial")
con.execute("SET geometry_always_xy = true")

query = """
SELECT
    ST_Distance_Sphere(
        ST_Point(77.5946, 12.9716),
        ST_Point(77.6046, 12.9716)
    ) AS distance_meters,
    ST_Distance_Sphere(
        ST_Point(77.5946, 12.9716),
       ST_Point(77.6046, 12.9716)
    ) <= 500 AS within_500m;
"""

result = con.execute(query).fetchdf()

print("GeoPulse 500-Meter Catchment Test")
print(result)

con.close()
