-- Set search path
SET search_path TO star_dwh;

-- Function to generate random store data
CREATE OR REPLACE FUNCTION generate_store_data(num_stores INT)
RETURNS void AS $$
DECLARE
    i INT;
    store_names TEXT[] := ARRAY['Mega', 'Super', 'Ultra', 'Prime', 'Elite', 'Premium', 'Grand', 'Royal', 'Imperial', 'Noble'];
    store_types TEXT[] := ARRAY['Mall', 'Plaza', 'Center', 'Market', 'Boutique', 'Emporium', 'Store', 'Shop', 'Outlet', 'Gallery'];
    cities TEXT[] := ARRAY['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
                         'London', 'Paris', 'Tokyo', 'Sydney', 'Toronto', 'Berlin', 'Rome', 'Madrid', 'Amsterdam', 'Singapore'];
    countries TEXT[] := ARRAY['United States', 'United Kingdom', 'France', 'Japan', 'Australia', 'Canada', 'Germany', 'Italy', 'Spain', 'Netherlands',
                            'Singapore', 'China', 'India', 'Brazil', 'Mexico', 'South Korea', 'Russia', 'Turkey', 'Saudi Arabia', 'Sweden'];
    country_codes TEXT[] := ARRAY['US', 'GB', 'FR', 'JP', 'AU', 'CA', 'DE', 'IT', 'ES', 'NL',
                                'SG', 'CN', 'IN', 'BR', 'MX', 'KR', 'RU', 'TR', 'SA', 'SE'];
    currency_codes TEXT[] := ARRAY['USD', 'GBP', 'EUR', 'JPY', 'AUD', 'CAD', 'EUR', 'EUR', 'EUR', 'EUR',
                                 'SGD', 'CNY', 'INR', 'BRL', 'MXN', 'KRW', 'RUB', 'TRY', 'SAR', 'SEK'];
BEGIN
    FOR i IN 1..num_stores LOOP
        INSERT INTO DimStore (
            store_id,
            name,
            city,
            country,
            country_code,
            primary_currency_code,
            valid_from,
            is_current
        ) VALUES (
            i,
            store_names[1 + floor(random() * array_length(store_names, 1))] || ' ' ||
            store_types[1 + floor(random() * array_length(store_types, 1))] || ' ' || i,
            cities[1 + floor(random() * array_length(cities, 1))],
            countries[1 + floor(random() * array_length(countries, 1))],
            country_codes[1 + floor(random() * array_length(country_codes, 1))],
            currency_codes[1 + floor(random() * array_length(currency_codes, 1))],
            CURRENT_TIMESTAMP,
            TRUE
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Generate 50 stores
SELECT generate_store_data(50);

-- Drop the function as it's no longer needed
DROP FUNCTION generate_store_data(INT); 