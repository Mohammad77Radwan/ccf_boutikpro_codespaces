# Option 2 - Installation locale

Ce guide décrit l'installation complète sur Windows, Linux, macOS et WSL.

## Outils nécessaires pour le CCF
- Git
- Python 3.11 ou version proche
- pip
- un environnement virtuel Python
- MySQL 8.x
- un terminal adapté au système
- l'éditeur PlantUML en ligne : `https://editor.plantuml.com/`
- éventuellement Visual Studio Code pour éditer les fichiers du projet

## 1. Clonage du dépôt
```bash
git clone <url-du-depot>
cd ccf_boutikpro_codespaces
```

## 2. Choix du script selon le système
- Windows CMD : `scripts/local/setup_windows.bat`
- Windows PowerShell : `scripts/local/setup_windows.ps1`
- Linux : `bash scripts/local/setup_linux.sh`
- macOS : `bash scripts/local/setup_macos.sh`
- WSL : `bash scripts/local/setup_wsl.sh`

Ces scripts préparent le projet local : environnement virtuel, dépendances Python et fichier `.env`.

## 3. Base de données MySQL
Créer une base MySQL, puis exécuter :

```bash
mysql -u root -p < sql/01_schema.sql
mysql -u root -p < sql/02_seed.sql
```

Adapter ensuite le fichier `.env` à votre installation locale.

## 4. PlantUML
Utiliser la version recommandée en ligne :

```text
https://editor.plantuml.com/
```

Copier ensuite le contenu final dans `uml/usecase.puml`.

## 5. Lancement des squelettes Python
```bash
python src/dbapi/main.py
python src/core/main.py
python src/orm/main.py
```

## 6. Consignes spécifiques par système

### Windows (.bat)
- Ouvrir **Invite de commandes**.
- Se placer dans le dépôt.
- Lancer :

```bat
scripts\local\setup_windows.bat
```

### Windows (.ps1)
- Ouvrir **PowerShell**.
- Autoriser l'exécution locale si nécessaire.
- Lancer :

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\local\setup_windows.ps1
```

### Linux
- Ouvrir un terminal.
- Lancer :

```bash
bash scripts/local/setup_linux.sh
```

### macOS
- Ouvrir Terminal.
- Lancer :

```bash
bash scripts/local/setup_macos.sh
```

### WSL
- Ouvrir votre distribution WSL.
- Installer MySQL côté Windows ou côté WSL selon votre organisation.
- Lancer :

```bash
bash scripts/local/setup_wsl.sh
```
