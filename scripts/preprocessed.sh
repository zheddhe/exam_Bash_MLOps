# =============================================================================
# Ce script preprocessed.sh exécute le programme src/preprocessed.py
# et enregistre les détails de son exécution dans le fichier de log
# logs/preprocessed.logs.
# =============================================================================

# Aller à la racine du projet (parent du dossier de ce script executé (argument 0))
cd "$(dirname "$0")/.." || exit 1

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/preprocessed.logs"
# python à utiliser : celui de l'environnement virtuel
PY=".venv/bin/python"
PY_SCRIPT="src/preprocessed.py"

mkdir -p "$LOG_DIR"

{
  echo "=== Lancement de preprocessed.sh ($(date '+%Y-%m-%d %H:%M:%S')) ==="
  # Lancement sans argument pour la chaine d'integration
  "$PY" "$PY_SCRIPT"
  RET=$?
  echo "=== Fin de preprocessed.sh (code retour: $RET) ==="
  exit $RET
} >> "$LOG_FILE" 2>&1