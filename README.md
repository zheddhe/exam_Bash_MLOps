# Linux & Bash

## Examen

Cet examen se décompose en 2 exercices :

- Le premier porte sur le langage bash (Obligatoire pour valider le module)
- Le second porte sur l'outil jq (Optionnelle)

### Examen : Bash - OBLIGATOIRE

Vous travaillez pour une entreprise qui vend des cartes graphiques et vous êtes chargé d'automatiser un processus de collecte de données, de prétraitement et d'entraînement d'un modèle de prédiction des ventes. Votre manager vous a confié un projet où vous devrez utiliser des outils Linux et des scripts pour automatiser chaque étape de ce processus.

Votre objectif est de concevoir un pipeline automatisé permettant de :

- **Collecter les données** provenant d'une API toutes les minutes,
- **Les enregistrer** dans un fichier CSV,
- **Les prétraiter**,
- **Entraîner un modèle de prédiction** sur ces données prétraitées.

L’ensemble de ce processus doit être automatisé en utilisant des **scripts Bash** pour enchaîner les différentes étapes, **Python** pour le traitement des données et l'entraînement du modèle, **cron** pour planifier l'exécution des scripts à intervalles réguliers, et un **Makefile** pour lancer toutes les étapes en une seule ligne de commande.

---

#### Mise en place de l'API

Dans ce cours, nous avons vu comment fonctionne un système Linux. Nous aurions pu all er encore plus en détail mais nous avons construit la base pour la suite du parcours. Suivez les instructions suivantes pour réaliser l'exercice.

<div class="alert alert-info"><i class="icon circle info"></i>
Exercice à réaliser <i>obligatoirement</i> sur la machine Linux mise à votre disposition.
</div>

> Connectez vous à votre machine et exécutez la commande suivante pour récupérer l'API

```shell
wget --no-cache https://dst-de.s3.eu-west-3.amazonaws.com/bash_fr/api.tar
```

Vous avez maintenant un fichier d'extension `.tar`. Il s'agit simplement d'une archive à la manière d'un fichier compressé `zip`, mais spécifique à Linux. Pour manipuler ce fichier, nous passons par la commande `tar` (pour _tape archiver_).
Pour tous les formats à base de tar, vous verrez que les options de tar sont les mêmes :

- c : crée l'archive
- x : extrait l'archive
- f : utilise le fichier donné en paramètre
- v : active le mode verbeux.

> Décompressez l'archive à l'aide de la commande suivante :

```shell
tar -xvf api.tar
```

L'extrait de l'archive vous dévoile le script _api_

> Lancez le script `api` après avoir donné les droits d'exécution :

```shell
chmod +x api
./api &
```

Notre API tourne maintenant en `localhost` (0.0.0.0) sur le port 5000.

<div class="alert alert-info"> <i class="icon circle info"></i>
Il est tout à fait possible de faire tourner l'API sans la mettre en arrière-plan mais l'exécution de cette dernière vous bloquera toute manipulation sur votre VM. Il faudra alors ouvrir un 2nd terminal et il faudra vous reconnecter à la VM et travailler avec le 2nd terminal uniquement.
</div>

Cette API nous dévoile les ventes par minutes du plus gros revendeurs de cartes graphiques sur les modèles rtx3060, rtx3070, rtx3080, rtx3090 et rx6700.
Il est possible de récupérer ces informations à l'aide de la commande **cURL**. Toutefois, il se peut que vous n'ayez pas cURL sur votre machine, pour remédier à cela, nous utilisons `apt` sur Linux.


#### Commande apt

`apt` est un gestionnaire de paquets qui contiennent différents logiciels que vous pouvez installer assez facilement avec une seule ligne de code.
Pour ce faire, nous pouvons faire comme suit :

```shell
apt install software_name
```

Dans les anciennes versions d'Ubuntu, vous aviez besoin d'utiliser `apt-get` au lieu de `apt`.
Dans la plupart des cas, vous avez besoin de `sudo` pour forcer les droits d'installation d'un logiciel.

Pour vous assurer que les paquets sont à jour, vous pouvez utiliser `sudo apt update` . Pour mettre à jour les
logiciels, vous pouvez utiliser `sudo apt upgrade` . Vous pouvez ajouter ou supprimer certains paquets et supprimer complètement un logiciel utilisant la fonction `apt purge`.

> Installez `curl` avec `apt`.

```shell
sudo apt-get update

sudo apt-get install curl
```

Maintenant que nous avons `curl`, expliquons l'outil.

#### Commande curl

cURL, qui signifie client URL est un outil de ligne de commande pour le transfert de fichiers avec une syntaxe URL. Il prend en charge un certain nombre de protocoles (HTTP, HTTPS, FTP, et bien d'autres). HTTP/HTTPS en fait un excellent candidat pour interagir avec les APIs.

On peut, par exemple, récupérer les ventes de RTX 3060 à l'aide de la commande suivante.

```shell
curl "http://0.0.0.0:5000/rtx3060"
```

### Mise en place de l'examen

- Créez un dossier exam_NOM où NOM est votre nom de famille.
- Ajoutez un dossier nommé exam_bash
- Clonez le Git pour les modalités de l'examen : 
```shell 
git clone https://github.com/DataScientest/exam_Bash_MLOps.git
```

En clonant le git, vous aurez l'arborescence suivante :
```txt
exam_NOM/
  ├── exam_bash/
      ├── data/
      │   ├── processed/              # Fichiers CSV prétraités
      │   └── raw/
      │       └── sales_data.csv      # Fichier CSV des données brutes (500 lignes)
      ├── logs/
      │   ├── test_logs/
      │   ├── collect.logs            # Logs de collecte des données
      │   ├── preprocessed.logs       # Logs de prétraitement des données
      │   └── train.logs              # Logs d'entraînement du modèle
      ├── model/                      # Stockage des modèles entraînés
      ├── scripts/
      │   ├── collect.sh              # Script de collecte des données (toutes les 2 minutes)
      │   ├── preprocessed.sh         # Script de prétraitement des données
      │   ├── train.sh                # Script d'entraînement du modèle
      │   └── cron.txt                # Fichier de configuration des tâches cron
      ├── src/
      │   ├── preprocessed.py         # Script de prétraitement des données (Python)
      │   └── train.py                # Script d'entraînement du modèle (Python)
      ├── tests/
      │   ├── test_collect.py         # Test de la collecte des données et de l'existence du CSV
      │   ├── test_model.py           # Test de l'entraînement du modèle et de l'existence du model.pkl
      │   └── test_preprocessed.py    # Test du bon prétraitement des données
      ├── Makefile                    # Makefile pour automatiser les tâches
      ├── README.md                   # Documentation du projet
      └── requirements.txt            # Dépendances du projet
```
> La version de Python utilisée pour ce projet est Python 3.12

Exécutez la commande suivante pour configurer l'environnement avec la bonne version de Python et installer automatiquement les bibliothèques nécessaires au bon fonctionnement des scripts fournis :
```bash
uv sync
```

N'oubliez pas d'activer votre environnement virtuel avant de commencer l'examen.

#### 1. **Collecte des Données**
Le processus commence par la collecte des données des ventes de cartes graphiques via une API que vous devrez interroger toutes les **3 minutes**. Ces données sont récupérées et stockées dans un fichier CSV situé dans le dossier `data/raw/`. 

#### 2. **Prétraitement des Données**
Une fois les données collectées, vous devrez appliquer un prétraitement. Ce prétraitement peut inclure :
- La suppression de valeurs manquantes ou incorrectes,
- La conversion des données dans le format approprié (par exemple, conversion de la date ou transformation des types de données),
- L'agrégation ou le filtrage des données si nécessaire.

Les résultats du prétraitement doivent être enregistrés dans un fichier CSV situé dans le dossier `data/processed/`.

#### 3. **Entraînement du Modèle**
Les données prétraitées serviront à entraîner un modèle de prédiction des ventes des cartes graphiques. Vous utiliserez probablement un modèle **XGBoost** pour cette tâche. Le modèle entraîné sera sauvegardé dans le dossier `model/` et sera utilisé pour faire des prédictions futures.

#### 4. **Automatisation via Cron**
Le processus complet (collecte des données, prétraitement et entraînement) doit être exécuté automatiquement. Vous utiliserez **cron** pour planifier les tâches à exécuter toutes les **3 minutes**. Un fichier `cron.txt` sera fourni pour configurer les tâches cron.

#### 5. **Utilisation d'un Makefile**
Un **Makefile** sera utilisé pour faciliter l'exécution des tâches et automatiser l'ensemble du pipeline avec la commande suivante :
```bash
make bash
```

#### Fichiers à Modifier

Vous trouverez dans les différents fichiers à modifier, les consignes correspondantes pour chaque tâche à réaliser.

1. **collect.sh**  
   Le script `collect.sh` doit être modifié pour automatiser la collecte des données toutes les 2 minutes.

2. **preprocessed.sh**  
   Le script `preprocessed.sh` doit être modifié pour lancer le prétraitement des données collectées.

3. **train.sh**  
   Le script `train.sh` doit être modifié pour entraîner le modèle avec les données prétraitées.

4. **cron.txt**  
   Vous devez configurer `cron.txt` pour exécuter automatiquement la collecte, le prétraitement et l'entraînement du modèle toutes les 3 minutes.

5. **preprocessed.py**  
   Le script `preprocessed.py` doit être modifié pour effectuer le prétraitement des données collectées (nettoyage, transformation des données, etc.).

6. **train.py**  
   Le script `train.py` doit être modifié pour entraîner le modèle de prédiction avec les données prétraitées.

7. **Makefile**  
   Le fichier `Makefile` doit être ajusté pour automatiser l’ensemble du processus avec une seule commande :
   ```bash
   make bash
   ```
8. **requirements.txt**
   Le fichier requirements.txt doit inclure uniquement les bibliothèques nécessaires pour l'exécution du programme, comme pandas, numpy, xgboost, etc.

Voici un diagramme qui résume brièvement le fonctionnement attendu du programme : 

<center><img src="https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/image.png" style="width:80%"/></center>


### Tests et Vérifications

Vous ne devez pas modifier les fichiers de test fournis. Ceux-ci valideront la conformité de votre travail.

- **Test de la collecte des données** (`test_collect.py`)
- **Test de l'entraînement du modèle** (`test_model.py`)
- **Test du prétraitement des données** (`test_preprocessed.py`)

Pour exécuter les tests, vous pouvez utiliser la commande suivante :
```bash
make tests
```

Cela va créer dans logs/tests_logs des fichiers test_*.logs.

Exemple de sortie des journaux (logs) générés par votre programme d'automatisation fonctionnel :

**test_collect.logs** : 
```txt
=== Début des tests (2025-04-30 15:21:03) ===
Début du test de structure du CSV
Fichier CSV chargé avec 520 lignes et 3 colonnes
Test réussi : Le CSV est valide.
Fin du test de structure du CSV
=== Fin des tests ===
```

**test_preprocessed.logs** : 
```txt
=== Début des tests (2025-04-30 15:21:19) ===
Début du test de structure du fichier prétraité
Fichier chargé : data/processed/sales_processed_20250430_1516.csv
Vérification colonne 'timestamp' : OK (non présente)
Vérification types entiers : OK (toutes les colonnes sont des entiers)
Test terminé pour le fichier prétraité.
=== Fin des tests ===
```

**test_model.logs** : 
```txt
=== Début des tests (2025-04-30 15:21:23) ===
Début du test de présence du fichier modèle
Test réussi : le fichier modèle existe.
=== Fin des tests (2025-04-30 15:21:23) ===
```

Une fois l’ensemble du programme exécuté (collecte, prétraitement, entraînement), voici ce que vous devez observer :

**data/raw** :
- Des fichiers CSV contenant les **données brutes de ventes** récupérées automatiquement depuis l'API.
- Ces fichiers suivent un nommage du type : `sales_YYYYMMDD_HHMM.csv`.

**data/processed/** :
- Des fichiers CSV contenant les **données prétraitées**, prêtes à être utilisées pour l'entraînement du modèle.
- Ces fichiers suivent un nommage du type : `sales_processed_YYYYMMDD_HHMM.csv`.

**model/** :
- Une ou plusieurs versions du **modèle entraîné**, enregistrées sous forme de fichier `.pkl`.
- Exemple : `model.pkl` ou `model_YYYYMMDD_HHMM.pkl`.

## Rendu final

> Créez une archive exam_NOM.tar

```bash
tar -cvf exam_NOM.tar exam_NOM
```

### Commande scp

La commande `scp` permet de transférer de manière sécurisée un fichier ou une archive (les dossiers ne sont pas transférables) via une connexion SSH.

Vous pouvez télécharger votre archive en exécutant la commande suivante `sur un terminal de votre propre machine`. 

```shell
scp -i "data_enginering_machine.pem" ubuntu@VOTRE_IP:~/exam_NOM.tar .
```

<div class="alert alert-info"> <i class="icon circle info"></i>
Plusieurs détails concernant la commande ci-dessus:
  <br>
  </br>
  - Lorsque vous ouvrez votre terminal sur votre ordinateur local pour transférer votre archive depuis la VM, précisez le chemin absolu vers votre fichier data_enginering_machine.pem
  <br>
  </br>
  - Votre archive sera téléchargée dans le même dossier où se trouve votre fichier data_enginering_machine.pem 
</div>

Une fois que vous avez téléchargé votre archive sur votre machine locale, vous pouvez l'envoyer en uploadant via l'onglet `Mes Exams`.

Bon courage !
