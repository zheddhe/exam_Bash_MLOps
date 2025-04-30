# Linux & Bash

## Examen

Cet examen se décompose en 2 exercices :

- Le premier porte sur le langage bash (Obligatoire pour valider le module)
- Le second porte sur l'outil jq (Optionnelle)

### Examen : Bash - OBLIGATOIRE


#### Mise en place de l'API

Dans ce cours, nous avons vu comment fonctionne un système Linux. Nous aurions pu aller encore plus en détail mais nous avons construit la base pour la suite du parcours. Suivez les instructions suivantes pour réaliser l'exercice.

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

> Créez un dossier exam_NOM ou NOM est votre nom de famille.

> Ajoutez un dossier nommé exam_bash

> Clonez le Git pour les modalités de l'examen : 
```shell 
git clone https://github.com/DataScientest/exam_Bash_MLOps.git
```

En clonant le git, vous aurez l'arborescence suivante :
```txt
exam_NOM/
  ├── exam_bash/
      ├── data/
        ├── processed/              # Dossier contenant les fichiers CSV prétraités
        └── raw/
            └── sales_data.csv      # Fichier CSV contenant 500 lignes de données brutes
      ├── logs/
          ├── test_logs/
          ├── collect.logs            # Fichier de logs pour la collecte des données
          ├── preprocessed.logs       # Fichier de logs pour le prétraitement des données collectées
          └── train.logs              # Fichier de logs pour l'entraînement du modèle avec les données prétraitées
      ├── model/                      # Dossier stockant toutes les versions des modèles entraînés
      ├── scripts/
          ├── collect.sh              # Script de collecte des données toutes les 2 minutes
          ├── preprocessed.sh         # Script lançant le prétraitement des données collectées
          ├── train.sh                # Script lançant l'entraînement du modèle avec les données prétraitées
          └── cron.txt                # Fichier de configuration pour les tâches cron 
      ├── src/
          ├── preprocessed.py         # Script de prétraitement des données collectées
          └── train.py                # Script d'entraînement du modèle avec les données prétraitées
      ├── tests/
          ├── test_collect.py         # Script de test pour vérifier la collecte des données et l'existence de fichiers CSV dans data/raw
          ├── test_model.py           # Script de test pour vérifier l'entraînement du modèle et l'existence du fichier model.pkl
          └── test_preprocessed.py    # Script de test pour vérifier le bon traitement des données                   
      ├── Makefile                    # Fichier Makefile pour automatiser les tâches
      ├── README.md                   # Fichier de documentation du projet
      └── requirements.txt            # Fichier contenant les dépendances du projet

```

> Vous trouverez dans les répertoires **scripts/** et **src/** l’ensemble des consignes et des éléments attendus à mettre en œuvre.
>
> Veuillez ne pas modifier les fichiers de tests. Vous pouvez toutefois les consulter pour mieux comprendre les vérifications attendues. Ces tests vous offrent un premier aperçu de la conformité de votre travail. Pour les exécuter, utilisez la commande `make tests`.

<br>

Votre fichier **cron.txt** doit être configuré pour exécuter automatiquement la collecte, le prétraitement et l'entraînement du modèle toutes les 3 minutes.

Configurez également votre **Makefile** afin qu'une simple commande `make bash` permette de lancer l'ensemble du programme : collecte des données, prétraitement et entraînement du modèle.

Votre fichier **requirements.txt** doit inclure uniquement les bibliothèques indispensables à l'exécution de votre programme, avec leurs versions précises.

Voici un diagramme qui résume brièvement le fonctionnement attendu du programme : 

<center><img src="https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/image.png" style="width:80%"/></center>

Plus qu'un exercice à faire pour valider ce module !

### 10.2 Examen : JQ - OPTIONNEL

#### Mise en place

Vous rentrerez les commandes dans un fichier exécutable (avec le droit d'exécution +x) `exam_jq.sh`. Afin de valider l'exercice, vous devez rendre le fichier `exam_jq.sh` ainsi qu'un fichier `res_jq.txt` alimenté à l'aide de la commande `./exam_jq.sh > res_jq.txt`. N'oubliez pas qu'un être humain corrigera vos fichiers, pensez donc à bien présenter vos résultats dans vos 2 fichiers.

> Créez dans votre dossier exam\_NOM, le dossier exam\_jq

> Rendez-vous dans celui-ci, et créez un fichier `exam_jq.sh` comme ceci :

```bash
#!/bin/bash

echo "1. Énoncé de la question 1"
<commande pour répondre>
echo "Commande : <commande pour répondre>"
echo "Réponse : réponse de la question 1 si demandé"
echo -e "\n---------------------------------\n"
...

echo "n. Énoncé de la question n"
<commande pour répondre>
echo "Commande : <commande pour répondre>"
echo "Réponse : réponse de la question n si demandé"
echo -e "\n---------------------------------\n"
```

- <commande pour répondre> : placez la commande liée à la question afin d'avoir le résultat de la commande dans le fichier `res_jq.txt`.

Remplissez les champs selon les questions évidemment. La réponse n'est pas le résultat du code mais votre interprétation de celui-ci.

#### Questions

Voici le fichier json qui va servir pour la réalisation de l'examen: 

```bash
wget https://dst-de.s3.eu-west-3.amazonaws.com/bash_fr/people.json
```

Seules les questions 1, 2 et 4 attendent une Réponse interprétée.

1. Affichez le nombre d'attributs par document ainsi que l'attribut name. Combien y a-t-il d'attribut par document ? N'affichez que les 12 premières lignes avec la commande head (notebook #2).

2. Combien y a-t-il de valeur "unknown" pour l'attribut "birth_year" ? Utilisez la commande tail afin d'isoler la réponse.

3. Affichez la date de création de chaque personnage et son nom. La date de création doit être de cette forme : l'année, le mois et le jour. N'affichez que les 10 premières lignes. (Pas de Réponse attendue)

4. Certains personnages sont nés en même temps. Retrouvez toutes les pairs d'ids (2 ids) des personnages nés en même temps.

5. Renvoyez le numéro du premier film (de la liste) dans lequel chaque personnage a été vu suivi du nom du personnage. N'affichez que les 10 premières lignes. (Pas de Réponse attendue)

#### Bonus

Ajoutez cette commande pour séparer la partie obligatoire de la partie optionnelle.

```bash
echo -e "\n----------------BONUS----------------\n"
```

Aucune Réponse n'est demandée.

Enregistrez chacune des commandes dans des fichiers au format : people_\<numéro\_de\_la\_question>.json
Ces fichiers doivent se trouver dans un dossier bonus/.

N'ajoutez rien au fichier `res_jq.txt`. Vous devez faire la redirection directement dans le fichier `exam_jq.sh`.

Les questions sont à réaliser depuis le fichier créé à la question précédente, sauf pour la question 6.

6. Supprimez les documents lorsque l'attribut height n'est pas un nombre.

7. Transformer l'attribut height en nombre.

8. Ne renvoyez que les personnages dont la taille est entre 156 et 171.

9. Renvoyez le plus petit individu de `people_8.json` et affichez cette phrase en une seule commande : "\<nom\_du\_personnage> is \<taille> tall"
Renvoyez la commande dans un fichier `people_9.txt` et non `.json`.

#### Rendu : JQ

Nous avons les dossiers et fichiers suivants :

- exam\_NOM/exam\_jq/exam\_jq.sh
- exam\_NOM/exam\_jq/res\_jq.txt
- exam\_NOM/exam\_jq/bonus/people\_\<6 à 9>.\<json ou txt>

#### Rendu final

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
