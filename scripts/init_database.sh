#!/bin/bash

# Database initialization script for SQLoslav
# This script runs all SQL initialization scripts in order

# Get database connection details from environment variables
DB_HOST=${POSTGRES_HOST:-"postgres"}
DB_PORT=${POSTGRES_PORT:-"5432"}
DB_NAME=${POSTGRES_DB:-"sqloslav_dwh"}
DB_USER=${POSTGRES_USER:-"admin"}
DB_PASSWORD=${POSTGRES_PASSWORD:-"admin"}

# Directory containing SQL scripts
SQL_DIR="../database/init"

# Function to execute a SQL script
execute_sql_script() {
    local script=$1
    echo "Executing $script..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -f "$SQL_DIR/$script"
    if [ $? -ne 0 ]; then
        echo "Error executing $script"
        exit 1
    fi
}

# Execute scripts in order
echo "Starting database initialization..."

# Create schemas
execute_sql_script "01_create_schemas.sql"

# Create star schema tables
execute_sql_script "02_create_star_schema.sql"

# Populate dimensions
execute_sql_script "03_populate_date_dimension.sql"
execute_sql_script "04_populate_currency_dimension.sql"
execute_sql_script "05_populate_customer_dimension.sql"
execute_sql_script "06_populate_product_dimension.sql"
execute_sql_script "07_populate_store_dimension.sql"
execute_sql_script "08_populate_employee_dimension.sql"

# Populate fact table
execute_sql_script "09_populate_fact_sales.sql"

echo "Database initialization completed successfully!" 