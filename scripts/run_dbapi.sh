#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python -m src.dbapi.main
