# Database Initialization Scripts

This directory contains the initialization scripts for the SQLoslav Data Warehouse. The scripts are executed in order based on their numeric prefix.

## Script Order and Purpose

1. `01_create_schemas.sql`
   - Creates the necessary schemas (oltp_3nf, star_dwh, snowflake_dwh)
   - Sets up permissions

2. `02_create_star_schema.sql`
   - Creates dimension and fact tables for the star schema
   - Sets up foreign key relationships
   - Creates performance indexes

3. `03_populate_date_dimension.sql`
   - Populates the date dimension with 3 years of data
   - Includes various date attributes and fiscal year calculation

4. `04_populate_currency_dimension.sql`
   - Populates the currency dimension with common world currencies
   - Includes currency codes and names

5. `05_populate_customer_dimension.sql`
   - Generates 1000 sample customers
   - Includes SCD (Slowly Changing Dimension) support

6. `06_populate_product_dimension.sql`
   - Generates 500 sample products
   - Includes various product types and price ranges

7. `07_populate_store_dimension.sql`
   - Generates 50 sample stores
   - Includes geographical information and primary currencies

8. `08_populate_employee_dimension.sql`
   - Generates 200 sample employees
   - Includes demographic information and birth countries

9. `09_populate_fact_sales.sql`
   - Generates 10,000 sample transactions
   - Each transaction has 1-5 items
   - Includes price calculations in both local and USD currencies

## Data Volume Summary

- Dates: ~1095 records (3 years)
- Currencies: 20 records
- Customers: 1000 records
- Products: 500 records
- Stores: 50 records
- Employees: 200 records
- Sales Facts: 30,000-50,000 records (10,000 transactions × 1-5 items each)

## Usage

These scripts are automatically executed when the PostgreSQL container starts up, as they are mounted in the `/docker-entrypoint-initdb.d` directory. The scripts will only run on the first container startup when the database is initialized. 