# Database initialization script for SQLoslav
# This script runs all SQL initialization scripts in order

# Get database connection details from environment variables
$DB_HOST = if ($env:POSTGRES_HOST) { $env:POSTGRES_HOST } else { "postgres" }
$DB_PORT = if ($env:POSTGRES_PORT) { $env:POSTGRES_PORT } else { "5432" }
$DB_NAME = if ($env:POSTGRES_DB) { $env:POSTGRES_DB } else { "sqloslav_dwh" }
$DB_USER = if ($env:POSTGRES_USER) { $env:POSTGRES_USER } else { "admin" }
$DB_PASSWORD = if ($env:POSTGRES_PASSWORD) { $env:POSTGRES_PASSWORD } else { "admin" }

# Directory containing SQL scripts
$SQL_DIR = "..\database\init"

# Function to execute a SQL script
function Execute-SqlScript {
    param (
        [string]$script
    )
    Write-Host "Executing $script..."
    $env:PGPASSWORD = $DB_PASSWORD
    $result = psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -f "$SQL_DIR\$script"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error executing $script"
        exit 1
    }
}

# Execute scripts in order
Write-Host "Starting database initialization..."

# Create schemas
Execute-SqlScript "01_create_schemas.sql"

# Create star schema tables
Execute-SqlScript "02_create_star_schema.sql"

# Populate dimensions
Execute-SqlScript "03_populate_date_dimension.sql"
Execute-SqlScript "04_populate_currency_dimension.sql"
Execute-SqlScript "05_populate_customer_dimension.sql"
Execute-SqlScript "06_populate_product_dimension.sql"
Execute-SqlScript "07_populate_store_dimension.sql"
Execute-SqlScript "08_populate_employee_dimension.sql"

# Populate fact table
Execute-SqlScript "09_populate_fact_sales.sql"

Write-Host "Database initialization completed successfully!" 