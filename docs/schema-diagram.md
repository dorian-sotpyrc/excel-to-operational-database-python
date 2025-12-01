# Schema diagram (example workbook)

This repository ships with a simple example schema that mirrors a common
"small business" Excel workbook with three sheets:

- `customers`
- `products`
- `orders`

The target relational schema is:

customers
---------
customer_id  (PK, int)
name         (string, not null)
email        (string, nullable)
joined_date  (datetime, nullable)

products
--------
product_id   (PK, int)
name         (string, not null)
category     (string, nullable)
unit_price   (decimal/float, nullable)

orders
------
order_id     (PK, int)
customer_id  (FK -> customers.customer_id)
product_id   (FK -> products.product_id)
order_date   (datetime, nullable)
quantity     (int, nullable)

**Relationships**

- One `customer` can have many `orders`.
- One `product` can appear in many `orders`.

This maps directly to the example configuration in
`config/config.example.yaml` and is ideal for illustrating the Excel →
relational database migration pipeline.
