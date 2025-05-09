-- Create schemas for the data warehouse
CREATE SCHEMA IF NOT EXISTS oltp_3nf;
CREATE SCHEMA IF NOT EXISTS star_dwh;
CREATE SCHEMA IF NOT EXISTS snowflake_dwh;

-- Set search path
SET search_path TO oltp_3nf, star_dwh, snowflake_dwh, public;

-- Grant permissions
GRANT USAGE ON SCHEMA oltp_3nf TO CURRENT_USER;
GRANT USAGE ON SCHEMA star_dwh TO CURRENT_USER;
GRANT USAGE ON SCHEMA snowflake_dwh TO CURRENT_USER; 