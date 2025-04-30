"""
-------------------------------------------------------------------------------
Ce script preprocessed.py récupère les données du dernier fichier CSV créé 
dans le dossier 'data/raw/'.

1. Il applique un prétraitement aux données
   
2. Les résultats du prétraitement sont enregistrés dans un nouveau fichier CSV 
   dans le dossier 'data/processed/', avec un nom au format 
   'sales_processed_YYYYMMDD_HHMM.csv'.
   
3. Toutes les étapes du prétraitement sont enregistrées dans le fichier 
   'logs/preprocessed.logs' afin de garantir un suivi détaillé du processus.

Les erreurs ou anomalies éventuelles sont également loguées pour assurer la traçabilité.
-------------------------------------------------------------------------------
"""

