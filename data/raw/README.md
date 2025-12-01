This folder is where your source Excel workbook should live.

By default, the configuration expects:

  data/raw/sample_workbook.xlsx

You can either:

1. Create a workbook named `sample_workbook.xlsx` with sheets
   `customers`, `products`, and `orders` that match the schema in
   `docs/schema-diagram.md`, or

2. Change `excel_path` in `config/config.yaml` to point to your own
   workbook file.

Example minimal structure:

- customers: customer_id, name, email, joined_date
- products: product_id, name, category, unit_price
- orders:   order_id, customer_id, product_id, order_date, quantity
