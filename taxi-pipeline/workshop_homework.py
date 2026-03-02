"""Script to analyze NYC taxi data from DuckDB database."""

import duckdb
import os

# Check the working directory and database files
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir()}")

# Try different database paths
possible_paths = [
    'taxi_pipeline.duckdb',
    './taxi_pipeline.duckdb',
    '/Users/xuehanyin/DE_training/data-engineer-homework/taxi-pipeline/taxi_pipeline.duckdb',
]

db_path = None
for path in possible_paths:
    if os.path.exists(path):
        db_path = path
        print(f"Found database at: {db_path}")
        break

if not db_path:
    print("Database not found!")
    exit(1)

# Connect to the database
conn = duckdb.connect(db_path)

# Get all schemas
schemas = conn.execute("SELECT schema_name FROM information_schema.schemata").fetchall()
print("\nSchemas in database:")
for schema in schemas:
    schema_name = schema[0]
    if schema_name not in ('information_schema', 'pg_catalog', 'memory'):
        print(f"  - {schema_name}")

print("\n" + "="*50 + "\n")

# Get all tables and their data
for schema in schemas:
    schema_name = schema[0]
    if schema_name in ('information_schema', 'pg_catalog', 'memory'):
        continue
    
    tables = conn.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}' AND table_type = 'BASE TABLE'").fetchall()
    
    for table in tables:
        table_name = table[0]
        
        # Skip internal dlt tables
        if table_name.startswith('_dlt_'):
            continue
        
        print(f"Table: {schema_name}.{table_name}")
        
        # Get column information
        cols = conn.execute(f"PRAGMA table_info(\"{schema_name}\".{table_name})").fetchall()
        date_columns = []
        
        for col in cols:
            col_name = col[1]
            col_type = col[2]
            # Look for date-like columns
            if 'date' in col_name.lower() or 'time' in col_name.lower():
                date_columns.append((col_name, col_type))
        
        if date_columns:
            print(f"  Date/Time columns: {date_columns}")
            for col_name, col_type in date_columns:
                result = conn.execute(f"SELECT MIN({col_name}) as min_date, MAX({col_name}) as max_date FROM \"{schema_name}\".{table_name}").fetchall()
                if result:
                    min_date, max_date = result[0]
                    print(f"    {col_name}: {min_date} to {max_date}")
        else:
            print("  No date/time columns found")
        
        # Show row count
        count = conn.execute(f"SELECT COUNT(*) FROM \"{schema_name}\".{table_name}").fetchone()[0]
        print(f"  Rows: {count}")
        print()

conn.close()

print("\n" + "="*50)
print("CREDIT CARD PAYMENT ANALYSIS")
print("="*50 + "\n")

# Reconnect to analyze payment methods
conn = duckdb.connect(db_path)

# Get payment method data from yellow taxi
print("Yellow Taxi Data:")
yellow_payment = conn.execute(
    """
    SELECT 
        payment_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
    FROM "taxi_pipeline_dataset".yellow_taxi_data
    GROUP BY payment_type
    ORDER BY count DESC
    """
).fetchall()

if yellow_payment:
    for row in yellow_payment:
        print(f"  {row[0]}: {row[1]} trips ({row[2]}%)")
    
    # Calculate credit card proportion
    total_yellow = conn.execute("SELECT COUNT(*) FROM \"taxi_pipeline_dataset\".yellow_taxi_data").fetchone()[0]
    # Check for 'Credit' payment type
    cc_yellow = conn.execute(
        """
        SELECT COUNT(*) FROM "taxi_pipeline_dataset".yellow_taxi_data 
        WHERE payment_type = 'Credit'
        """
    ).fetchone()[0]
    
    print(f"\n  Credit Card Proportion (Yellow): {cc_yellow}/{total_yellow} = {(cc_yellow/total_yellow*100):.2f}%")
else:
    print("  No payment type column found in yellow taxi data")

print("\nGreen Taxi Data:")
green_payment = conn.execute(
    """
    SELECT 
        payment_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
    FROM "taxi_pipeline_dataset".green_taxi_data
    GROUP BY payment_type
    ORDER BY count DESC
    """
).fetchall()

if green_payment:
    for row in green_payment:
        print(f"  {row[0]}: {row[1]} trips ({row[2]}%)")
    
    # Calculate credit card proportion
    total_green = conn.execute("SELECT COUNT(*) FROM \"taxi_pipeline_dataset\".green_taxi_data").fetchone()[0]
    # Check for 'Credit' payment type
    cc_green = conn.execute(
        """
        SELECT COUNT(*) FROM "taxi_pipeline_dataset".green_taxi_data 
        WHERE payment_type = 'Credit'
        """
    ).fetchone()[0]
    
    print(f"\n  Credit Card Proportion (Green): {cc_green}/{total_green} = {(cc_green/total_green*100):.2f}%")
else:
    print("  No payment type column found in green taxi data")

conn.close()

print("\n" + "="*50)
print("TOTAL TIPS ANALYSIS")
print("="*50 + "\n")

# Reconnect to analyze tips
conn = duckdb.connect(db_path)

# Calculate total tips from yellow taxi
print("Yellow Taxi Tips:")
yellow_tips = conn.execute(
    """
    SELECT 
        ROUND(SUM(COALESCE(tip_amt, 0)), 2) as total_tips,
        COUNT(*) as num_records,
        ROUND(AVG(COALESCE(tip_amt, 0)), 2) as avg_tips
    FROM "taxi_pipeline_dataset".yellow_taxi_data
    """
).fetchall()

if yellow_tips:
    total_tips_yellow, count_yellow, avg_tips_yellow = yellow_tips[0]
    print(f"  Total Tips: ${total_tips_yellow}")
    print(f"  Number of Trips: {count_yellow}")
    print(f"  Average Tips per Trip: ${avg_tips_yellow}")

# Calculate total tips from green taxi
print("\nGreen Taxi Tips:")
green_tips = conn.execute(
    """
    SELECT 
        ROUND(SUM(COALESCE(tip_amt, 0)), 2) as total_tips,
        COUNT(*) as num_records,
        ROUND(AVG(COALESCE(tip_amt, 0)), 2) as avg_tips
    FROM "taxi_pipeline_dataset".green_taxi_data
    """
).fetchall()

if green_tips:
    total_tips_green, count_green, avg_tips_green = green_tips[0]
    print(f"  Total Tips: ${total_tips_green}")
    print(f"  Number of Trips: {count_green}")
    print(f"  Average Tips per Trip: ${avg_tips_green}")

# Calculate combined total tips
if yellow_tips and green_tips:
    combined_total_tips = (total_tips_yellow or 0) + (total_tips_green or 0)
    print(f"\n  COMBINED TOTAL TIPS (Yellow + Green): ${combined_total_tips}")

conn.close()
