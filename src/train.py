"""
-------------------------------------------------------------------------------
Ce script exécute l'entraînement d'un modèle XGBoost pour prédire les ventes de
cartes graphiques à partir des données prétraitées.

1. Il commence par rechercher le dernier fichier CSV prétraité dans le dossier
   'data/processed/'.
2. Si un modèle standard (model.pkl) n'existe pas, il charge les données, les
   divise en ensembles d'entraînement et de test, entraîne un modèle sur ces
   données, l'évalue, puis le sauvegarde dans 'model/model.pkl'.
3. Si un modèle standard existe déjà, il entraîne un nouveau modèle sur les
   données les plus récentes, l'évalue, puis sauvegarde le modèle dans le dossier
   'model/' sous formats : model_YYYYMMDD_HHMM.pkl.
4. Les métriques de performance (RMSE, MAE, R²) sont affichées et sauvegardées dans
   le fichier de log.
5. Des erreurs éventuelles sont gérées et signalées dans les logs.

Les modèles sont sauvegardés dans le dossier 'model/' avec le nom 'model.pkl' pour
le modèle standard et avec un horodatage pour les versions ultérieures.
Les métriques du modèle sont enregistrées dans les logs du script.
-------------------------------------------------------------------------------
"""

import argparse
# import glob
import logging
# import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import joblib


# --------------------------------------------------------------------------- #
# Constantes de chemins
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = ROOT / "data" / "processed"
MODEL_DIR = ROOT / "model"
LOGS_DIR = ROOT / "logs"
TRAIN_LOG = LOGS_DIR / "train.logs"


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
def setup_logging() -> None:
    """
    Mise en place du logger en niveau INFO
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=TRAIN_LOG,
        level=logging.INFO,
        format="[%(asctime)s] | %(levelname)s | %(message)s",
    )


# --------------------------------------------------------------------------- #
# Utilitaires
# --------------------------------------------------------------------------- #
def find_latest_processed_csv(processed_dir: Path) -> Path:
    candidates = sorted(
        processed_dir.glob("sales_processed_*.csv"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(
            f"Aucun fichier prétraité trouvé dans {processed_dir} "
            "(attendu: sales_processed_YYYYMMDD_HHMM.csv)"
        )
    return candidates[0]


def infer_X_y(df: pd.DataFrame, mode: str = 'first') -> Tuple[pd.DataFrame, pd.Series]:
    """
    Tente d'inférer une matrice X et une cible y selon deux heuristiques,
    pour être robuste au format 'wide' (plusieurs colonnes numérique déjà prétraitées).

    Modes :
      first) y = première colonne numérique ; X = autres numériques
      all)   y = somme des colonnes numériques ; X = colonnes numériques
    """
    df_num = df.select_dtypes(include=[np.number]).copy()

    # Cas "first" : première colonne numérique comme cible
    if mode == 'first':
        first_num = df_num.columns[0]
        y = df_num[first_num].astype(float)
        X = df_num.drop(columns=[first_num]).astype(float)
        return X, y

    # Cas "all" par défaut : on construit une cible = total (modelisation triviale)
    y = df_num.sum(axis=1).astype(float)
    X = df_num.astype(float)
    return X, y


def build_model() -> object:
    # Paramètres simples et sûrs (pas de GPU requis)
    return XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=0,
    )


def train_and_eval(X: pd.DataFrame, y: pd.Series) -> Tuple[object, dict]:
    # Séparation train test en random ici
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Instanciation et entraînement
    model = build_model()
    model.fit(X_train, y_train)  # type: ignore

    # Évaluation
    y_pred = model.predict(X_test)  # type: ignore

    # Calcul des métriques
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mae = float(mean_absolute_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))
    metrics = {"rmse": rmse, "mae": mae, "r2": r2}

    return model, metrics


def save_model(model: object, standard_path: Path) -> Path:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if not standard_path.exists():
        # Première sauvegarde : model.pkl
        joblib.dump(model, standard_path)
        return standard_path

    # Sinon, sauvegarde horodatée
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    dated = MODEL_DIR / f"model_{stamp}.pkl"
    joblib.dump(model, dated)
    return dated


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    # Ajout d'un parser d'argument pour fichier de sortie et d'entree explicite
    parser = argparse.ArgumentParser(
        description="Entraîne un modèle de prédiction des ventes sur les données prétraitées."
    )
    parser.add_argument(
        "--processed-dir",
        type=str,
        default=str(DATA_PROCESSED),
        help="Dossier contenant les CSV prétraités (défaut: data/processed).",
    )
    args = parser.parse_args(argv)

    # Configuration de la log
    setup_logging()

    # Corps de l'entraînement
    logging.info("=== Début de l'entraînement du modèle ===")
    try:
        # Récupération du fichier CSF le plus récent
        processed_dir = Path(args.processed_dir)
        processed_dir.mkdir(parents=True, exist_ok=True)
        latest_csv = find_latest_processed_csv(processed_dir)
        logging.info(f"Dernier CSV prétraité : {latest_csv}")

        # Lecture du fichier dans un dataframe
        df = pd.read_csv(latest_csv)
        logging.info(f"Fichier chargé : {latest_csv.name} | shape={df.shape}")

        # Séparation variable cible et variable explicatives
        X, y = infer_X_y(df)
        logging.info(f"Jeu de données pour entraînement : X={X.shape}, y={y.shape}")

        # Entrainement et évaluation du modèle
        model, metrics = train_and_eval(X, y)
        logging.info(
            f"Métriques — RMSE: {metrics['rmse']:.4f} | "
            f"MAE: {metrics['mae']:.4f} | R²: {metrics['r2']:.4f}"
        )

        # Sauvegarde du modèle
        standard_model_path = MODEL_DIR / "model.pkl"
        saved_path = save_model(model, standard_model_path)
        logging.info(f"Modèle sauvegardé : {saved_path}")

        logging.info("=== Fin de l'entraînement du modèle ===")
        return 0

    except FileNotFoundError as e:
        logging.error(str(e))
        print(str(e))
        return 2
    except Exception as e:
        logging.exception("Erreur lors de l'entraînement du modèle")
        print(f"Erreur lors de l'entraînement du modèle: {e}")
        return 1


# Pour l'appel par script avec code retour SystemExit
if __name__ == "__main__":
    raise SystemExit(main())
