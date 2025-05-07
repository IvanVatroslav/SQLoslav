-- Set search path
SET search_path TO star_dwh;

-- Function to generate random product data
CREATE OR REPLACE FUNCTION generate_product_data(num_products INT)
RETURNS void AS $$
DECLARE
    i INT;
    product_types TEXT[] := ARRAY['Electronics', 'Clothing', 'Food', 'Books', 'Home & Garden', 'Sports', 'Toys', 'Beauty', 'Health', 'Automotive'];
    product_names TEXT[] := ARRAY['Smartphone', 'Laptop', 'T-shirt', 'Jeans', 'Cereal', 'Novel', 'Garden Tool', 'Basketball', 'Action Figure', 'Shampoo',
                                'Vitamins', 'Car Parts', 'Headphones', 'Dress', 'Snacks', 'Textbook', 'Furniture', 'Tennis Racket', 'Board Game', 'Makeup'];
    min_price DECIMAL := 10.00;
    max_price DECIMAL := 1000.00;
BEGIN
    FOR i IN 1..num_products LOOP
        INSERT INTO DimProduct (
            product_id,
            name,
            type,
            price_usd,
            valid_from,
            is_current
        ) VALUES (
            i,
            product_names[1 + floor(random() * array_length(product_names, 1))] || ' ' || i,
            product_types[1 + floor(random() * array_length(product_types, 1))],
            round((min_price + random() * (max_price - min_price))::numeric, 2),
            CURRENT_TIMESTAMP,
            TRUE
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Generate 500 products
SELECT generate_product_data(500);

-- Drop the function as it's no longer needed
DROP FUNCTION generate_product_data(INT); 