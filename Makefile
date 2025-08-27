SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

# Dossiers & fichiers
SCRIPTS_DIR := scripts
DATA_DIR    := data
RAW_DIR     := $(DATA_DIR)/raw
PROC_DIR    := $(DATA_DIR)/processed
MODEL_DIR   := model
LOGS_DIR    := logs
TESTS_DIR   := tests
CRON_FILE   := $(SCRIPTS_DIR)/cron.txt

.PHONY: all bash tests cron uncron help clean

# Enchaîne les targets pour la chaine complete avec test
all: ## Exécute le pipeline complet puis les tests
	$(MAKE) bash
	$(MAKE) tests

bash: | $(RAW_DIR) $(PROC_DIR) $(MODEL_DIR) $(LOGS_DIR) ## Collecte + prétraitement + entraînement
	@echo "==> RUN: collect"
	$(SCRIPTS_DIR)/collect.sh
	@echo "==> RUN: preprocessed"
	$(SCRIPTS_DIR)/preprocessed.sh
	@echo "==> RUN: train"
	$(SCRIPTS_DIR)/train.sh

tests: ## Lance la batterie de tests
	pytest $(TESTS_DIR)/test_collect.py
	pytest $(TESTS_DIR)/test_preprocessed.py
	pytest $(TESTS_DIR)/test_model.py

cron: ## Installe la crontab depuis scripts/cron.txt
	crontab $(CRON_FILE)
	@echo "Crontab installée depuis $(CRON_FILE)."

uncron: ## Supprime la crontab active
	crontab -r
	@echo "Crontab supprimée."

# Création paresseuse des dossiers (order-only prerequisites)
$(RAW_DIR) $(PROC_DIR) $(MODEL_DIR) $(LOGS_DIR):
	mkdir -p $@

help: ## Affiche cette aide
	@awk 'BEGIN{FS=":.*##"; printf "\nTargets disponibles:\n\n"} /^[a-zA-Z0-9_.-]+:.*##/{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2} /^.DEFAULT_GOAL/{print ""} ' $(MAKEFILE_LIST)

clean: ## Nettoie artefacts communs (optionnel)
	rm -rf $(MODEL_DIR)/*.pkl
	find $(LOGS_DIR) -type f -name "*.log" -delete 2>/dev/null || true