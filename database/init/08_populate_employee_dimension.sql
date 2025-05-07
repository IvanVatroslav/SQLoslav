-- Set search path
SET search_path TO star_dwh;

-- Function to generate random employee data
CREATE OR REPLACE FUNCTION generate_employee_data(num_employees INT)
RETURNS void AS $$
DECLARE
    i INT;
    first_names TEXT[] := ARRAY['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth',
                              'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen'];
    last_names TEXT[] := ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                             'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'];
    countries TEXT[] := ARRAY['United States', 'United Kingdom', 'France', 'Japan', 'Australia', 'Canada', 'Germany', 'Italy', 'Spain', 'Netherlands',
                            'Singapore', 'China', 'India', 'Brazil', 'Mexico', 'South Korea', 'Russia', 'Turkey', 'Saudi Arabia', 'Sweden'];
    country_codes TEXT[] := ARRAY['US', 'GB', 'FR', 'JP', 'AU', 'CA', 'DE', 'IT', 'ES', 'NL',
                                'SG', 'CN', 'IN', 'BR', 'MX', 'KR', 'RU', 'TR', 'SA', 'SE'];
    min_age INT := 20;
    max_age INT := 65;
    birth_date DATE;
BEGIN
    FOR i IN 1..num_employees LOOP
        -- Generate random birth date for an employee between min_age and max_age
        birth_date := CURRENT_DATE - ((min_age + floor(random() * (max_age - min_age + 1)))::text || ' years')::interval;
        
        INSERT INTO DimEmployee (
            employee_id,
            first_name,
            last_name,
            full_name,
            date_of_birth,
            country_of_birth,
            country_of_birth_code,
            valid_from,
            is_current
        ) VALUES (
            i,
            first_names[1 + floor(random() * array_length(first_names, 1))],
            last_names[1 + floor(random() * array_length(last_names, 1))],
            first_names[1 + floor(random() * array_length(first_names, 1))] || ' ' || 
            last_names[1 + floor(random() * array_length(last_names, 1))],
            birth_date,
            countries[1 + floor(random() * array_length(countries, 1))],
            country_codes[1 + floor(random() * array_length(country_codes, 1))],
            CURRENT_TIMESTAMP,
            TRUE
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Generate 200 employees
SELECT generate_employee_data(200);

-- Drop the function as it's no longer needed
DROP FUNCTION generate_employee_data(INT); 