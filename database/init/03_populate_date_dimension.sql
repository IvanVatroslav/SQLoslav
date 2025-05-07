-- Set search path
SET search_path TO star_dwh;

-- Function to populate date dimension
CREATE OR REPLACE FUNCTION populate_date_dimension(start_date DATE, end_date DATE)
RETURNS void AS $$
DECLARE
    current_date DATE;
    date_key INT;
    day INT;
    month INT;
    month_name VARCHAR(9);
    quarter INT;
    year INT;
    day_of_week INT;
    day_name VARCHAR(9);
    is_weekend BOOLEAN;
    fiscal_year INT;
BEGIN
    current_date := start_date;
    
    WHILE current_date <= end_date LOOP
        date_key := TO_CHAR(current_date, 'YYYYMMDD')::INT;
        day := EXTRACT(DAY FROM current_date);
        month := EXTRACT(MONTH FROM current_date);
        month_name := TO_CHAR(current_date, 'Month');
        quarter := EXTRACT(QUARTER FROM current_date);
        year := EXTRACT(YEAR FROM current_date);
        day_of_week := EXTRACT(DOW FROM current_date);
        day_name := TO_CHAR(current_date, 'Day');
        is_weekend := EXTRACT(DOW FROM current_date) IN (0, 6);
        fiscal_year := CASE 
            WHEN EXTRACT(MONTH FROM current_date) >= 4 
            THEN EXTRACT(YEAR FROM current_date) 
            ELSE EXTRACT(YEAR FROM current_date) - 1 
        END;
        
        INSERT INTO DimDate (
            date_key, date, day, month, month_name, quarter, year,
            day_of_week, day_name, is_weekend, is_holiday, fiscal_year
        ) VALUES (
            date_key, current_date, day, month, month_name, quarter, year,
            day_of_week, day_name, is_weekend, FALSE, fiscal_year
        );
        
        current_date := current_date + INTERVAL '1 day';
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Populate date dimension for the next 3 years
SELECT populate_date_dimension(
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '3 years'
);

-- Drop the function as it's no longer needed
DROP FUNCTION populate_date_dimension(DATE, DATE); 