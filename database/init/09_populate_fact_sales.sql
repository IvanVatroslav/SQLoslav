-- Set search path
SET search_path TO star_dwh;

-- Function to generate random sales data
CREATE OR REPLACE FUNCTION generate_sales_data(num_transactions INT)
RETURNS void AS $$
DECLARE
    i INT;
    j INT;
    transaction_date DATE;
    transaction_time TIMESTAMP;
    items_per_transaction INT;
    customer_count INT;
    product_count INT;
    store_count INT;
    employee_count INT;
    currency_count INT;
    selected_customer_key INT;
    selected_product_key INT;
    selected_store_key INT;
    selected_employee_key INT;
    selected_currency_key INT;
    selected_date_key INT;
    selected_hour INT;
    selected_minute INT;
    selected_quantity INT;
    selected_price_usd DECIMAL;
    currency_rate DECIMAL;
BEGIN
    -- Get counts of dimension records
    SELECT COUNT(*) INTO customer_count FROM DimCustomer;
    SELECT COUNT(*) INTO product_count FROM DimProduct;
    SELECT COUNT(*) INTO store_count FROM DimStore;
    SELECT COUNT(*) INTO employee_count FROM DimEmployee;
    SELECT COUNT(*) INTO currency_count FROM DimCurrency;

    FOR i IN 1..num_transactions LOOP
        -- Generate random transaction date within the last year
        transaction_date := CURRENT_DATE - (floor(random() * 365) || ' days')::interval;
        selected_hour := floor(random() * 24);
        selected_minute := floor(random() * 60);
        transaction_time := transaction_date + (selected_hour || ' hours')::interval + (selected_minute || ' minutes')::interval;
        selected_date_key := TO_CHAR(transaction_date, 'YYYYMMDD')::INT;
        
        -- Generate random number of items per transaction (1-5)
        items_per_transaction := 1 + floor(random() * 5);
        
        -- Select random dimension keys
        selected_customer_key := 1 + floor(random() * customer_count);
        selected_store_key := 1 + floor(random() * store_count);
        selected_employee_key := 1 + floor(random() * employee_count);
        selected_currency_key := 1 + floor(random() * currency_count);
        
        -- Generate multiple items for this transaction
        FOR j IN 1..items_per_transaction LOOP
            -- Select random product
            selected_product_key := 1 + floor(random() * product_count);
            -- Get product price
            SELECT price_usd INTO selected_price_usd FROM DimProduct WHERE product_key = selected_product_key;
            -- Generate random quantity (1-10)
            selected_quantity := 1 + floor(random() * 10);
            -- Generate random currency rate (0.8-1.2 of USD)
            currency_rate := 0.8 + random() * 0.4;
            
            INSERT INTO FactSales (
                transaction_id,
                transaction_item_id,
                customer_key,
                product_key,
                store_key,
                employee_key,
                date_key,
                currency_key,
                transaction_hour,
                transaction_minute,
                quantity,
                price_per_unit_local,
                price_per_unit_usd,
                total_price_local,
                total_price_usd,
                transaction_time
            ) VALUES (
                i,
                j,
                selected_customer_key,
                selected_product_key,
                selected_store_key,
                selected_employee_key,
                selected_date_key,
                selected_currency_key,
                selected_hour,
                selected_minute,
                selected_quantity,
                round((selected_price_usd * currency_rate)::numeric, 2),
                selected_price_usd,
                round((selected_price_usd * currency_rate * selected_quantity)::numeric, 2),
                round((selected_price_usd * selected_quantity)::numeric, 2),
                transaction_time
            );
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Generate 10000 transactions (will result in 30000-50000 fact records)
SELECT generate_sales_data(10000);

-- Drop the function as it's no longer needed
DROP FUNCTION generate_sales_data(INT); 