#!/bin/bash
# ==============================================================================# ==============================================================================
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
#   Commentaires : J'ai implémenté en proposant plutôt d'ajouter les données
#   au plus recent fichier sales_*.csv sinon on perdrait des données
#   en partant systématiquement de sales_data.csv ?
# ==============================================================================

set -euo pipefail

# --- Constantes et chemins ----------------------------------------------------
MODELS=("rtx3060" "rtx3070" "rtx3080" "rtx3090" "rx6700")
API_BASE="http://0.0.0.0:5000"

RAW_DIR="data/raw"
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/collect.logs"

# Nom du fichier de sortie : sales_YYYYMMDD_HHMM.csv (heure locale pour le nom)
OUT_STAMP="$(date +"%Y%m%d_%H%M")"
OUTPUT_CSV="${RAW_DIR}/sales_${OUT_STAMP}.csv"

# Timestamp ISO UTC pour les nouvelles mesures
NOW_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# --- Fonctions utilitaires ---
log() {
  # Format lisible avec date locale
  printf "[%s] %s\n" "$(date +"%Y-%m-%d %H:%M:%S")" "$*" | tee -a "$LOG_FILE" >/dev/null
}

ensure_dirs() {
  # Création si besoin des repertoires de travail utilisé (log et data/raw)
  mkdir -p "$RAW_DIR" "$LOG_DIR"
  # Assure l'existence du fichier de log
  touch "$LOG_FILE"
}

copy_or_init_csv() {
  # Trouve le plus récent sales_*.csv ; sinon en crée un nouveau avec entête
  local latest
  # nullglob pour éviter que le pattern littéral ne sorte si aucun match
  shopt -s nullglob
  # tri par date décroissante ; prendre le premier si dispo
  latest=$(ls -1t "${RAW_DIR}"/sales_*.csv 2>/dev/null | head -n1 || true)
  shopt -u nullglob

  if [[ -n "${latest:-}" ]]; then
    if [[ ! -f "$OUTPUT_CSV" ]]; then
        cp "$latest" "$OUTPUT_CSV"
        log "Copie du CSV source ${latest} vers ${OUTPUT_CSV}"
    else
        log "Fichier cible ${OUTPUT_CSV} déjà présent, copie ignorée"
    fi
  else
	# fallback si aucun fichier trouvé
    local new_file="${RAW_DIR}/sales_${OUT_STAMP}.csv"
    log "Aucune fichier sales trouvé. Initialisation d'un nouveau avec entête : ${new_file}."
  fi
}

fetch_sales() {
  # Appelle l'endpoint local qui retourne un nombre (sans horodatage)
  local model="$1"
  local url="${API_BASE}/${model}"
  local resp

  # --silent: pas de baratin ; --show-error: mais affiche erreurs si échec
  # --fail: code de retour ≠0 si HTTP >= 400 ; --max-time: timeout dur
  if ! resp="$(curl --silent --show-error --fail --max-time 5 "$url")"; then
    log "ERREUR requête API (${url})"
    echo ""
    return 1
  fi

  # Nettoyage et validation
  resp="$(echo "$resp" | tr -d '\r\n[:space:]')"
  if [[ ! "$resp" =~ ^[0-9]+$ ]]; then
    log "ERREUR réponse invalide pour ${model} : '${resp}' (attendu entier)"
    echo ""
    return 1
  fi
  
  echo "$resp"
}

append_batch() {
  log "Début de la collecte."
  log "Fichier cible (append) : ${OUTPUT_CSV}"
  log "Horodatage (UTC) : ${NOW_UTC}"
  log "Modèles interrogés : ${MODELS[*]}"

  # Début avec une nouvelle ligne
  echo "" >> "$OUTPUT_CSV"
  for model in "${MODELS[@]}"; do
    sales="$(fetch_sales "$model" || true)"
    if [[ -z "$sales" ]]; then
      sales=0
      log "Avertissement | ${model} -> fallback à 0 (échec API)"
    fi
    echo "${NOW_UTC},${model},${sales}" >> "$OUTPUT_CSV"
    log "Résultat | ${model} -> ${sales}"
  done

  # petit récap
  local n_lines n_cols
  n_lines="$(wc -l < "$OUTPUT_CSV" | tr -d ' ')"
  n_cols="$(head -n1 "$OUTPUT_CSV" | awk -F',' '{print NF}')"
  log "Résumé fichier : ${OUTPUT_CSV} | lignes=${n_lines} colonnes=${n_cols}"
  log "Fin de la collecte."
}

summary_counts() {
  # Compte lignes/colonnes pour vérification rapide
  local n_lines n_cols
  n_lines="$(wc -l < "$OUTPUT_CSV" | tr -d ' ')"
  # Nombre de colonnes d'après l'entête
  n_cols="$(head -n1 "$OUTPUT_CSV" | awk -F',' '{print NF}')"
  log "Résumé fichier : ${OUTPUT_CSV} | lignes=${n_lines} colonnes=${n_cols}"
}

# --- Procédure principale ---
main() {
  ensure_dirs
  log "=== Début de la tâche de collecte ==="
  copy_or_init_csv
  append_batch
  log "=== Fin de la tâche de collecte ==="
}

main "$@"
