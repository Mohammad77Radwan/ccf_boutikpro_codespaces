#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

bash .devcontainer/install_mysql_client.sh

python -m pip install -r requirements.txt

until mysql -h db -uroot -prootpwd -e "SELECT 1" >/dev/null 2>&1; do
  echo "En attente de MySQL..."
  sleep 2
done

mysql -h db -uroot -prootpwd -e "CREATE DATABASE IF NOT EXISTS boutikpro_ccf CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -h db -uroot -prootpwd boutikpro_ccf < sql/01_schema.sql
mysql -h db -uroot -prootpwd boutikpro_ccf < sql/02_seed.sql
mysql -h db -uroot -prootpwd boutikpro_ccf < sql/student_upgrade.sql

echo "Base initialisée avec les modifications étudiantes."
