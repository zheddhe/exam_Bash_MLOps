# -----------------------------------------------------------------------------
# Ce script train.sh exécute le programme Python src/train.py
# Ce programme entraîne un modèle de prédiction et enregistre le modèle final
# dans le répertoire model/. Le script enregistre également tous les détails
# de l'exécution dans le fichier logs/train.logs.
# -----------------------------------------------------------------------------

# Aller à la racine du projet (parent du dossier de ce script exécuté)
cd "$(dirname "$0")/.." || exit 1

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/train.logs"
PY_SCRIPT="src/train.py"

mkdir -p "$LOG_DIR"

{
  echo "=== Lancement de train.sh ($(date '+%Y-%m-%d %H:%M:%S')) ==="
  # Lancement sans argument pour la chaîne d'intégration
  python3 "$PY_SCRIPT"
  RET=$?
  echo "=== Fin de train.sh (code retour: $RET) ==="
  exit $RET
} >> "$LOG_FILE" 2>&1