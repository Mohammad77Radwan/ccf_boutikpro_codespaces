# BoutikPro - CCF Python / MySQL / Modélisation BTS SIO SLAM

## Documentation du CCF

| Partie | Documentation | Contenu | Statut |
|---|---|---|---|
| Démarrage | [START-HERE](START-HERE.md) | Feuille de route de l'étudiant | OK |
| Sujet | [SUBJECT](SUBJECT.md) | Énoncé complet du CCF | OK |
| Option 1 - Installation distante | [Guide installation distante](docs/INSTALLATION-CODESPACE.md) | Lancement avec GitHub Codespaces et outils en ligne | OK |
| Option 2 - Installation locale | [Guide installation locale](docs/INSTALLATION-LOCALE.md) | Installation sur poste personnel | OK |
| CRUD Python | [Guide CRUD](docs/guides/CRUD_PYTHON.md) | Rappels Create / Read / Update / Delete | OK |
| DB-API | [Guide DB-API](docs/guides/PYTHON_DB_API.md) | Connexion native MySQL en Python | OK |
| SQLAlchemy Core | [Guide Core](docs/guides/SQLALCHEMY_CORE.md) | Requêtes SQLAlchemy Core | OK |
| SQLAlchemy ORM | [Guide ORM](docs/guides/SQLALCHEMY_ORM.md) | Mapping classes / tables | OK |
| MCD / MLD | [Guide Modélisation](docs/guides/MCD_MLD.md) | Passage du MCD au MLD | OK |
| UML - Cas d'utilisation | [Guide UML](docs/phase-01/01-diagramme-cas-utilisation.md) | TP PlantUML sur le diagramme de l'application | OK |
| Questions | [Questions du TP](docs/questions/QUESTIONS-TP.md) | Questions de cours liées au TP | OK |
| Évaluation | [Grille](docs/grille_evaluation.md) | Barème indicatif | OK |

BoutikPro est une application de gestion commerciale simplifiée . Le projet est centré sur :

- la modélisation UML et Merise ;
- la création et la modification d'une base MySQL ;
- le passage MCD → MLD ;
- la programmation Python connectée à la base ;
- la mise en œuvre d'un CRUD ;
- le choix d'un des trois modes d'accès aux données :
  - Python DB-API
  - SQLAlchemy Core
  - SQLAlchemy ORM

## Image du MCD de référence

![MCD BoutikPro](assets/MCD_schema_entite_association.jpg)

## Public cible
- Étudiants de BTS SIO SLAM 2e année
- Formateurs en développement et base de données
- Enseignants souhaitant un support CCF lançable sous Codespaces ou en local

## Objectifs pédagogiques
1. Analyser un besoin métier à partir d'un contexte professionnel
2. Relier diagramme de cas d'utilisation, MCD et base relationnelle
3. Créer et faire évoluer une base MySQL
4. Programmer un CRUD Python sur une base réelle
5. Justifier les choix techniques et documenter le travail réalisé

## Installation rapide

### Option 1 : installation distante

Cette option repose sur GitHub Codespaces pour l'environnement d'exécution et sur l'éditeur PlantUML en ligne pour la modélisation UML.

1. Ouvrir ce dépôt dans GitHub.
2. Cliquer sur **Code** puis **Codespaces**.
3. Choisir **Create codespace on main**.
4. Attendre l'initialisation automatique.
5. Dans le terminal, exécuter :

```bash
bash scripts/setup.sh
bash scripts/check_db.sh
```

6. Ouvrir l'éditeur PlantUML en ligne à l'adresse suivante :

```text
https://editor.plantuml.com/
```

7. Lire dans cet ordre :
- [START-HERE.md](START-HERE.md)
- [SUBJECT.md](SUBJECT.md)
- [docs/INSTALLATION-CODESPACE.md](docs/INSTALLATION-CODESPACE.md)
- [docs/phase-01/01-diagramme-cas-utilisation.md](docs/phase-01/01-diagramme-cas-utilisation.md)
- [docs/guides/CRUD_PYTHON.md](docs/guides/CRUD_PYTHON.md)
- le guide du mode choisi :
  - [docs/guides/PYTHON_DB_API.md](docs/guides/PYTHON_DB_API.md)
  - [docs/guides/SQLALCHEMY_CORE.md](docs/guides/SQLALCHEMY_CORE.md)
  - [docs/guides/SQLALCHEMY_ORM.md](docs/guides/SQLALCHEMY_ORM.md)

### Option E : installation locale

Cette option permet de travailler hors Codespaces, sur Windows, Linux, macOS ou WSL.

1. Lire le guide complet : [docs/INSTALLATION-LOCALE.md](docs/INSTALLATION-LOCALE.md)
2. Choisir ensuite le script adapté à votre système :
- Windows CMD : `scripts/local/setup_windows.bat`
- Windows PowerShell : `scripts/local/setup_windows.ps1`
- Linux : `scripts/local/setup_linux.sh`
- macOS : `scripts/local/setup_macos.sh`
- WSL : `scripts/local/setup_wsl.sh`
3. Ouvrir ensuite PlantUML :

```text
https://editor.plantuml.com/
```

## Analyse fonctionnelle du TP

### Acteurs métier retenus
- Utilisateur (acteur générique)
- Employé commercial
- Gestionnaire catalogue
- Gestionnaire fournisseurs
- Comptable

### Cas d'utilisation couverts par le sujet
- gérer les clients ;
- attribuer une carte de fidélité ;
- enregistrer une commande ;
- ajouter des produits dans une commande ;
- gérer les produits et leurs catégories ;
- gérer les fournisseurs et leurs catégories ;
- générer une facture à partir d'une commande ;
- enregistrer une recommandation entre clients.

### Modèle de données cible
Le sujet prend appui sur le MCD fourni dans `assets/MCD_schema_entite_association.jpg`.

Principales entités :
- `Client`
- `Commande`
- `Carte_fidelite`
- `Facture`
- `Produit`
- `Categorie_produit`
- `Fournisseur`
- `Categorie_fournisseur`

Principales associations :
- `Contient`
- `Livre`
- `Recommande`

## Structure du projet

```text
ccf-boutikpro-codespaces/
├── README.md
├── START-HERE.md
├── SUBJECT.md
├── TEACHER_NOTES.md
├── .env.example
├── requirements.txt
├── .devcontainer/
├── assets/
│   └── MCD_schema_entite_association.jpg
├── docs/
│   ├── INSTALLATION-CODESPACE.md
│   ├── INSTALLATION-LOCALE.md
│   ├── README-CODESPACE.md
│   ├── TROUBLESHOOTING.md
│   ├── grille_evaluation.md
│   ├── phase-01/
│   │   ├── 00-README.md
│   │   ├── 01-diagramme-cas-utilisation.md
│   │   └── 02-livrables-uml.md
│   ├── phase-02/
│   ├── phase-03/
│   ├── guides/
│   └── questions/
├── scripts/
│   ├── setup.sh
│   ├── check_db.sh
│   └── local/
│       ├── setup_windows.bat
│       ├── setup_windows.ps1
│       ├── setup_linux.sh
│       ├── setup_macos.sh
│       └── setup_wsl.sh
├── sql/
├── src/
└── uml/
    └── usecase.puml
```
