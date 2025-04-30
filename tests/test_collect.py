import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
from contextlib import redirect_stdout

def get_latest_sales_csv():
    """
    Trouve le dernier fichier CSV créé dans le dossier data/raw
    avec le format sales_YYYYMMDD_HHMM.csv
    """
    data_dir = Path("data/raw")
    if not data_dir.exists():
        raise FileNotFoundError(f"Le dossier {data_dir} n'existe pas.")
    
    csv_files = list(data_dir.glob("sales_*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Aucun fichier 'sales_*.csv' trouvé dans {data_dir}")
    
    return max(csv_files, key=lambda f: f.stat().st_mtime)

def test_sales_csv_structure():
    log_file_path = Path("logs/tests_logs/test_collect.logs")
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file_path, "a") as f, redirect_stdout(f):
        print(f"\n=== Début des tests ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
        print("Début du test de structure du CSV")

        try:
            latest_csv = get_latest_sales_csv()
            df = pd.read_csv(latest_csv)
            print(f"Fichier CSV chargé avec {df.shape[0]} lignes et {df.shape[1]} colonnes")

            assert len(df.columns) == 3, f"Le CSV doit contenir exactement 3 colonnes, trouvé {len(df.columns)}"
            assert 'sales' in df.columns, "Le CSV doit contenir une colonne 'sales'"
            assert not df['sales'].isnull().any(), "La colonne 'sales' ne doit pas contenir de valeurs NaN"
            assert np.all(np.equal(np.floor(df['sales']), df['sales'])), "La colonne 'sales' doit contenir uniquement des entiers"
            assert (df['sales'] >= 0).all(), "La colonne 'sales' doit contenir uniquement des valeurs positives"

            print("Test réussi : Le CSV est valide.")
        
        except Exception as e:
            print(f"Test échoué avec l'erreur: {str(e)}")
            raise  

        print("Fin du test de structure du CSV")
        print(f"=== Fin des tests ===\n")
