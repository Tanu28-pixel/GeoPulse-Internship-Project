import duckdb

# Connect to GeoPulse database
con = duckdb.connect("geopulse.duckdb")

# Create project schemas
con.execute("CREATE SCHEMA IF NOT EXISTS raw_data")
con.execute("CREATE SCHEMA IF NOT EXISTS analytics")

# Display available schemas
print("GeoPulse Database Setup Successful!")
print(con.execute("SHOW SCHEMAS").fetchdf())

con.close()