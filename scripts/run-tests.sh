#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ALLURE_RESULTS_DIR="$PROJECT_ROOT/allure-results"

cd "$PROJECT_ROOT"

# Limpiar resultados anteriores
rm -rf "$ALLURE_RESULTS_DIR"
mkdir -p "$ALLURE_RESULTS_DIR"

echo "Running Behave tests with Allure..."

# Ejecutar Behave con Allure formatter
# NOTA: no se usa -o con pretty, solo con Allure
behave -f allure_behave.formatter:AllureFormatter \
       -o "$ALLURE_RESULTS_DIR" \
       "$@"
