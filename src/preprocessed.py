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

import argparse
import glob
import logging
import os
from datetime import datetime
from pathlib import Path
import sys
import pandas as pd

# --------------------------------------------------------------------------- #
# Constantes de chemins
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "preprocessed.logs"


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
def _setup_logging() -> None:
    """
    Mise en place du logger en niveau INFO
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="[%(asctime)s] | %(levelname)s | %(message)s",
    )


# --------------------------------------------------------------------------- #
# Utilitaires
# --------------------------------------------------------------------------- #
def _find_latest_raw_csv(explicit_path: Path | None = None) -> Path:
    """
    Trouve le dernier CSV créé/modifié dans data/raw/
    (ou le chemin explicite s'il est fourni).
    """
    if explicit_path:
        p = explicit_path if explicit_path.is_absolute() else ROOT / explicit_path
        if not p.exists():
            raise FileNotFoundError(f"Fichier explicite introuvable: {p}")
        return p

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    candidates = sorted(glob.glob(str(RAW_DIR / "*.csv")))
    if not candidates:
        fallback = RAW_DIR / "sales_data.csv"
        if fallback.exists():
            return fallback
        raise FileNotFoundError("Aucun fichier CSV brut trouvé dans data/raw/.")

    latest = max(candidates, key=os.path.getmtime)
    return Path(latest)


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Données d'entrée au format long: ['timestamp','model','sales'].
    Étapes:
      - Valide les colonnes attendues
      - Convertit 'sales' en numérique, remplace NaN par 0, clippe les négatifs à 0
      - Agrège par (timestamp, model) via somme (pas obligatoire en extraction à la minute)
      - Pivot en large (colonnes=modèles), remplace NaN par 0
      - Force toutes les colonnes en entiers non négatifs (int64)
      - Supprime 'timestamp' dans la sortie
    """
    # Verification des colonnes
    expected = {"timestamp", "model", "sales"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV brut: {sorted(missing)}")

    # Nettoyage sales -> numérique >=0
    sales = pd.to_numeric(df["sales"], errors="coerce").fillna(0)
    sales = sales.clip(lower=0)

    # Normalisation des modèles (sécurité contre espaces/upper)
    models = df["model"].astype(str).str.strip().str.lower()

    # Agrégation par timestamp & model (si doublons)
    tmp = (
        pd.DataFrame({
            "timestamp": pd.to_datetime(df["timestamp"], errors="coerce"),
            "model": models,
            "sales": sales,
        })
        .dropna(subset=["timestamp", "model"])
        .groupby(["timestamp", "model"], as_index=False)["sales"]
        .sum()
    )

    # Pivot long -> large : une colonne par modèle
    wide = tmp.pivot_table(index="timestamp", columns="model", values="sales", aggfunc="sum")

    # On veut uniquement des colonnes entières, pas de timestamp dans la sortie
    if wide is None or wide.empty:
        # Si aucune donnée exploitable, df vide
        return pd.DataFrame()

    # Remplace NaN par 0, s'assure non-négatif, conversion en int
    wide = wide.fillna(0).clip(lower=0)

    # cast en int64 (après arrondi sécurisé)
    wide = wide.round(0).astype("int64")

    # Supprime la dimension d'index 'timestamp' pour l'export (les tests exigent 'timestamp' absent)
    wide = wide.reset_index(drop=True)

    return wide


def _save_processed(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    if output_path is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_path = PROC_DIR / f"sales_processed_{stamp}.csv"
    df.to_csv(output_path, index=False)
    return output_path


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    # Ajout d'un parser d'argument pour fichier de sortie et d'entree explicite
    parser = argparse.ArgumentParser(
        description="Prétraitement ventes GPU: long (timestamp,model,sales) -> large (modèles)."
    )
    parser.add_argument("--input", type=str, default=None,
                        help="Chemin d'entrée explicite (optionnel).")
    parser.add_argument("--output", type=str, default=None,
                        help="Chemin de sortie explicite (optionnel).")
    args = parser.parse_args()

    # Configuration de la log
    _setup_logging()

    # Corps du prétraitement
    logging.info("=== Début du prétraitement ===")
    try:
        # Récupération du fichier CSF le plus récent
        input_csv = _find_latest_raw_csv(Path(args.input) if args.input else None)
        logging.info("Chargement du fichier brut : %s", input_csv)
        df = pd.read_csv(input_csv)
        logging.info("Fichier brut chargé avec %d lignes et %d colonnes", df.shape[0], df.shape[1])

        # Nettoyage du dataframe
        df_clean = _clean_dataframe(df)
        logging.info("Après pivot & nettoyage : %d lignes et %d colonnes",
                     df_clean.shape[0], df_clean.shape[1])

        # Vérification exigée pour passer les tests
        has_timestamp = "timestamp" in df_clean.columns
        all_int = all(pd.api.types.is_integer_dtype(t) for t in df_clean.dtypes)
        logging.info("Vérification colonne 'timestamp' : %s", "OK (non présente)"
                     if not has_timestamp else "NON OK (présente)")
        logging.info("Vérification types entiers : %s", "OK (toutes les colonnes sont des entiers)"
                     if all_int else "NON OK")

        # Enregistrement du fichier
        out_path = Path(args.output) if args.output else None
        out_csv = _save_processed(df_clean, out_path)
        logging.info("Fichier prétraité enregistré : %s", out_csv)
        logging.info("=== Fin du prétraitement ===")

        return 0

    except Exception as e:
        logging.info("ERREUR pendant le prétraitement : %s", e)
        logging.info("=== Fin du prétraitement (avec erreurs) ===")
        print(f"[preprocessed.py] Erreur: {e}", file=sys.stderr)
        return 1


# Pour l'appel par script avec code retour SystemExit
if __name__ == "__main__":
    raise SystemExit(main())
