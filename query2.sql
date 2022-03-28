WITH
  sales_by_client_and_product_type AS (
  SELECT
    client_id,
    product.product_type,
    CASE
      WHEN product.product_type = "MEUBLE" THEN SUM(prod_price * prod_qty)
    END AS ventes_meuble,
    CASE
      WHEN product.product_type = "DECO" THEN SUM(prod_price * prod_qty)
    END AS ventes_deco,
  FROM
    transaction
  JOIN
   product_nomenclature as product
  ON
    transaction.prod_id=product.product_id
  WHERE
    date BETWEEN "2019-01-01"
    AND "2019-12-31"
  GROUP BY
    client_id,
    product.product_type )
SELECT
  client_id,
  SUM(ventes_meuble) AS ventes_meuble,
  SUM(ventes_deco) AS ventes_deco,
FROM
  sales_by_client_and_product_type
GROUP BY
  client_id