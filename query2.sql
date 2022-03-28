SELECT
  client_id,
  SUM(CASE
      WHEN product.product_type = "MEUBLE" THEN prod_price * prod_qty
  END) AS ventes_meuble,
  SUM(CASE
      WHEN product.product_type = "DECO" THEN prod_price * prod_qty
  END) AS ventes_deco,
FROM
  transaction
JOIN
  product_nomenclature AS product
ON
  transaction.prod_id=product.product_id
WHERE
  date BETWEEN "2019-01-01" AND "2019-12-31"
GROUP BY
  client_id