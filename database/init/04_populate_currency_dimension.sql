-- Set search path
SET search_path TO star_dwh;

-- Populate currency dimension with common currencies
INSERT INTO DimCurrency (currency_id, code, name, valid_from, is_current)
VALUES 
    (1, 'USD', 'US Dollar', CURRENT_TIMESTAMP, TRUE),
    (2, 'EUR', 'Euro', CURRENT_TIMESTAMP, TRUE),
    (3, 'GBP', 'British Pound', CURRENT_TIMESTAMP, TRUE),
    (4, 'JPY', 'Japanese Yen', CURRENT_TIMESTAMP, TRUE),
    (5, 'AUD', 'Australian Dollar', CURRENT_TIMESTAMP, TRUE),
    (6, 'CAD', 'Canadian Dollar', CURRENT_TIMESTAMP, TRUE),
    (7, 'CHF', 'Swiss Franc', CURRENT_TIMESTAMP, TRUE),
    (8, 'CNY', 'Chinese Yuan', CURRENT_TIMESTAMP, TRUE),
    (9, 'INR', 'Indian Rupee', CURRENT_TIMESTAMP, TRUE),
    (10, 'BRL', 'Brazilian Real', CURRENT_TIMESTAMP, TRUE),
    (11, 'RUB', 'Russian Ruble', CURRENT_TIMESTAMP, TRUE),
    (12, 'KRW', 'South Korean Won', CURRENT_TIMESTAMP, TRUE),
    (13, 'SGD', 'Singapore Dollar', CURRENT_TIMESTAMP, TRUE),
    (14, 'NZD', 'New Zealand Dollar', CURRENT_TIMESTAMP, TRUE),
    (15, 'MXN', 'Mexican Peso', CURRENT_TIMESTAMP, TRUE),
    (16, 'HKD', 'Hong Kong Dollar', CURRENT_TIMESTAMP, TRUE),
    (17, 'TRY', 'Turkish Lira', CURRENT_TIMESTAMP, TRUE),
    (18, 'SAR', 'Saudi Riyal', CURRENT_TIMESTAMP, TRUE),
    (19, 'SEK', 'Swedish Krona', CURRENT_TIMESTAMP, TRUE),
    (20, 'NOK', 'Norwegian Krone', CURRENT_TIMESTAMP, TRUE); 