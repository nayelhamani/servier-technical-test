# servier-technical-test
Rendu test technique Nayel HAMANI

<h3>Installation :</h3>
<h4>Pré-requis :</h4>
virtualenv <br>
python 3.7

```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py
```
Ce code permet de lire les fichiers plats dans le folder "ressources" et les agréger d'après les règles de gestion pour sortir un json en résultat puis extraire le nom du journal qui mentionne le plus de médicaments différents à partir du json produit.

Le json de résultat se présente sous la forme d'une liste de dict. Un dict représente un médicament et pour chaque médicament on retrouve "mention" une liste qui répertorie là où ce medicament a été cité. 
Une mention est définie par une date, un type d'article (pubmed, clinical_trials ou journal), le titre de la publication (sauf si c'est une mention dans un journal) et le nom du journal.

sample du résultat :
```
[
  {
    "atccode": "6302001",
    "drug": "isoprenaline",
    "mention": [
      {
        "date_mention": "2020/01/01",
        "article_type": "pubmed",
        "title": "gold nanoparticles synthesized from euphorbia fischeriana root by green route method alleviates the isoprenaline hydrochloride induced myocardial infarction in rats.",
        "journal": "journal of photochemistry and photobiology. b, biology"
      },
      {
        "date_mention": "2020/01/01",
        "article_type": "journal",
        "title": NaN,
        "journal": "journal of photochemistry and photobiology. b, biology"
      }
    ]
  },
  {
    "atccode": "a01ad",
    "drug": "epinephrine",
    ...
  }
]
```
4. Traitement ad-hoc 

_Extraire depuis le json produit par la data pipeline le nom du journal qui mentionne le plus de médicaments différents ?_

"journal of emergency nursing" avec 2 médicaments différents

6. Pour aller plus loin

_Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?_

Les éléments à considérer sont mon besoin et mes contraintes. Si ma volumétrie augmente, quelles sont les repercussions sur mon ingestion ?
Y'a-t-il des contraintes de temps ? La donnée doit être disponible rapidement, dans ce cas je vais avoir besoin d'améliorer ma pipeline afin d'accélerer mon traitement.
Y'a-t-il des contraintes de coût ? Dois-je évoluer vers une infrastructure la plus efficace ou la plus cost efficient.
Le tout en m'assurant d'avoir une infrastructure maintenable afin de limiter la dette technique.
Enfin on peut aussi évoquer les contraintes technologiques tel qu'une infrastructure on premise ou cloud qui vont orienter mes choix de solution.

_Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de telles volumétries ?_

Les pistes amelioration pour pouvoir gérer une plus grosse volumétrie de données sont les suivantes :

Utiliser des formats de fichier plus adaptés a de gros volume de données (Parquet, Avro, ORC)

Utiliser un framework de traitement en parallèle afin d'améliorer les performances : exemple réécrire le code sous forme de job Spark

Conteneuriser le code via Docker et utiliser Kubernetes afin d'automatiser la scalabilité

Plus globalement, utiliser des services serverless sur le cloud pour assurer la scalabilité

II) SQL

2. Première partie du test
```
SELECT
    date,
    SUM(prod_price * prod_qty) AS ventes
FROM
    transaction
WHERE
    date BETWEEN "2019-01-01"AND "2019-12-31"
GROUP BY
    date
ORDER BY
    date ASC
```

3. Seconde partie du test
```
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
```
