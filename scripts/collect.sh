# ==============================================================================
# Script : collect.sh
# Description :
#   Ce script interroge une API afin de récupérer les ventes des modèles de cartes graphiques suivants :
#     - rtx3060
#     - rtx3070
#     - rtx3080
#     - rtx3090
#     - rx6700
#
#   Les données collectées sont ajoutées à une copie du fichier :
#     data/raw/sales_data.csv
#
#   Le fichier de sortie est sauvegardé au format :
#     data/raw/sales_YYYYMMDD_HHMM.csv
#   avec les colonnes suivantes :
#     timestamp, model, sales
#
#   L’activité de collecte (requêtes, modèles interrogés, résultats, erreurs)
#   est enregistrée dans un fichier de log :
#     logs/collect.logs
#
#   Le log est lisible et doit inclure :
#     - La date et l’heure de chaque requête
#     - Les modèles interrogés
#     - Les ventes récupérées
#     - Les éventuelles erreurs
# ==============================================================================


