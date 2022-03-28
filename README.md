# servier-technical-test
Rendu test technique Nayel HAMANI




6. Pour aller plus loin

_Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?_

Les éléments à considérer sont mon besoin et mes contraintes. Si ma volumétrie augmente, quelles sont les repercussions sur mon ingestion ?
Y'a-t-il des contraintes de temps ? La donnée doit être disponible rapidement, dans ce cas j'aurais besoin d'améliorer ma pipeline afin d'accelerer mon traitement.
Y'a-t-il des contraintes de cout ? Dois-je evoluer vers une infrastructure la plus efficace ou la plus cost efficient.
Le tout en m'assurant d'avoir une infrastructure maintenable afin de limiter la dette technique.
Enfin on peut aussi évoquer les contraintes technologiques tel que infrastructure on premise ou cloud qui vont orienter mes choix de solutions.

_Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de telles volumétries ?_

Les pistes amelioration pour pouvoir gérer une plus grosse volumétrie de données sont les suivantes :

Utiliser des formats de fichier plus adaptés a de gros volume de données (Parquet, Avro, ORC)

Utiliser un framework de traitement en parallèle afin d'améliorer les performances : exemple réecrire le code sous forme de jobs Spark

Conteneuriser le code via Docker et utiliser Kubernetes afin d'automatiser la scalabilité

Plus globalement, utiliser des services serverless sur le cloud pour assurer la scalabilité

