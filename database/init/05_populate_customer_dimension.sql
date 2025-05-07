-- Set search path
SET search_path TO star_dwh;

-- Function to generate random customer data
CREATE OR REPLACE FUNCTION generate_customer_data(num_customers INT)
RETURNS void AS $$
DECLARE
    i INT;
    first_names TEXT[] := ARRAY['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'James', 'Emma', 'Robert', 'Olivia',
                              'William', 'Sophia', 'Daniel', 'Isabella', 'Matthew', 'Mia', 'Joseph', 'Charlotte', 'Andrew', 'Amelia'];
    last_names TEXT[] := ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                             'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'];
BEGIN
    FOR i IN 1..num_customers LOOP
        INSERT INTO DimCustomer (
            customer_id,
            first_name,
            last_name,
            full_name,
            valid_from,
            is_current
        ) VALUES (
            i,
            first_names[1 + floor(random() * array_length(first_names, 1))],
            last_names[1 + floor(random() * array_length(last_names, 1))],
            first_names[1 + floor(random() * array_length(first_names, 1))] || ' ' || 
            last_names[1 + floor(random() * array_length(last_names, 1))],
            CURRENT_TIMESTAMP,
            TRUE
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Generate 1000 customers
SELECT generate_customer_data(1000);

-- Drop the function as it's no longer needed
DROP FUNCTION generate_customer_data(INT); 