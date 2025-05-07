-- Set search path
SET search_path TO star_dwh;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS FactSales CASCADE;
DROP TABLE IF EXISTS DimCustomer CASCADE;
DROP TABLE IF EXISTS DimProduct CASCADE;
DROP TABLE IF EXISTS DimStore CASCADE;
DROP TABLE IF EXISTS DimEmployee CASCADE;
DROP TABLE IF EXISTS DimDate CASCADE;
DROP TABLE IF EXISTS DimCurrency CASCADE;

-- 1. DimDate - Time dimension table
CREATE TABLE DimDate
(
    date_key    INT PRIMARY KEY,
    date        DATE       NOT NULL UNIQUE,
    day         INT        NOT NULL,
    month       INT        NOT NULL,
    month_name  VARCHAR(9) NOT NULL,
    quarter     INT        NOT NULL,
    year        INT        NOT NULL,
    day_of_week INT        NOT NULL,
    day_name    VARCHAR(9) NOT NULL,
    is_weekend  BOOLEAN    NOT NULL,
    is_holiday  BOOLEAN    NOT NULL DEFAULT FALSE,
    fiscal_year INT        NOT NULL
);

-- 2. DimCustomer - Customer dimension with SCD support
CREATE TABLE DimCustomer
(
    customer_key SERIAL PRIMARY KEY,
    customer_id  INT          NOT NULL,
    first_name   VARCHAR(50)  NOT NULL,
    last_name    VARCHAR(50)  NOT NULL,
    full_name    VARCHAR(101) NOT NULL,
    valid_from   TIMESTAMP    NOT NULL,
    valid_to     TIMESTAMP    NULL,
    is_current   BOOLEAN      NOT NULL DEFAULT TRUE
);

-- 3. DimProduct - Product dimension with denormalized product type
CREATE TABLE DimProduct
(
    product_key SERIAL PRIMARY KEY,
    product_id  INT            NOT NULL,
    name        VARCHAR(100)   NOT NULL,
    type        VARCHAR(50)    NOT NULL,
    price_usd   DECIMAL(10, 2) NOT NULL,
    valid_from  TIMESTAMP      NOT NULL,
    valid_to    TIMESTAMP      NULL,
    is_current  BOOLEAN        NOT NULL DEFAULT TRUE
);

-- 4. DimStore - Store dimension with denormalized geography
CREATE TABLE DimStore
(
    store_key             SERIAL PRIMARY KEY,
    store_id              INT          NOT NULL,
    name                  VARCHAR(100) NOT NULL,
    city                  VARCHAR(100) NOT NULL,
    country               VARCHAR(100) NOT NULL,
    country_code          CHAR(2)      NOT NULL,
    primary_currency_code CHAR(3)      NOT NULL,
    valid_from            TIMESTAMP    NOT NULL,
    valid_to              TIMESTAMP    NULL,
    is_current            BOOLEAN      NOT NULL DEFAULT TRUE
);

-- 5. DimEmployee - Employee dimension with denormalized birth country
CREATE TABLE DimEmployee
(
    employee_key          SERIAL PRIMARY KEY,
    employee_id           INT          NOT NULL,
    first_name            VARCHAR(50)  NOT NULL,
    last_name             VARCHAR(50)  NOT NULL,
    full_name             VARCHAR(101) NOT NULL,
    date_of_birth         DATE         NOT NULL,
    country_of_birth      VARCHAR(100) NOT NULL,
    country_of_birth_code CHAR(2)      NOT NULL,
    valid_from            TIMESTAMP    NOT NULL,
    valid_to              TIMESTAMP    NULL,
    is_current            BOOLEAN      NOT NULL DEFAULT TRUE
);

-- 6. DimCurrency - Currency dimension
CREATE TABLE DimCurrency
(
    currency_key SERIAL PRIMARY KEY,
    currency_id  INT         NOT NULL,
    code         CHAR(3)     NOT NULL,
    name         VARCHAR(50) NOT NULL,
    valid_from   TIMESTAMP   NOT NULL,
    valid_to     TIMESTAMP   NULL,
    is_current   BOOLEAN     NOT NULL DEFAULT TRUE
);

-- 7. FactSales - Fact table for sales transactions
CREATE TABLE FactSales
(
    sales_key            BIGSERIAL PRIMARY KEY,
    transaction_id       INT            NOT NULL,
    transaction_item_id  INT            NOT NULL,
    customer_key         INT            NOT NULL,
    product_key          INT            NOT NULL,
    store_key            INT            NOT NULL,
    employee_key         INT            NOT NULL,
    date_key             INT            NOT NULL,
    currency_key         INT            NOT NULL,
    transaction_hour     INT            NOT NULL,
    transaction_minute   INT            NOT NULL,
    quantity             INT            NOT NULL,
    price_per_unit_local DECIMAL(10, 2) NOT NULL,
    price_per_unit_usd   DECIMAL(10, 2) NOT NULL,
    total_price_local    DECIMAL(10, 2) NOT NULL,
    total_price_usd      DECIMAL(10, 2) NOT NULL,
    transaction_time     TIMESTAMP      NOT NULL,
    FOREIGN KEY (customer_key) REFERENCES DimCustomer (customer_key),
    FOREIGN KEY (product_key) REFERENCES DimProduct (product_key),
    FOREIGN KEY (store_key) REFERENCES DimStore (store_key),
    FOREIGN KEY (employee_key) REFERENCES DimEmployee (employee_key),
    FOREIGN KEY (date_key) REFERENCES DimDate (date_key),
    FOREIGN KEY (currency_key) REFERENCES DimCurrency (currency_key)
);

-- Create indexes for better query performance
CREATE INDEX idx_factsales_customer ON FactSales(customer_key);
CREATE INDEX idx_factsales_product ON FactSales(product_key);
CREATE INDEX idx_factsales_store ON FactSales(store_key);
CREATE INDEX idx_factsales_employee ON FactSales(employee_key);
CREATE INDEX idx_factsales_date ON FactSales(date_key);
CREATE INDEX idx_factsales_currency ON FactSales(currency_key);
CREATE INDEX idx_factsales_transaction_time ON FactSales(transaction_time); 