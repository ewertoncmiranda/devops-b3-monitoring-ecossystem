#!/bin/bash
# Script de setup para o projeto DevOps Study
# Instala dependências e prepara ambiente para testes

set -e

echo "=========================================="
echo "🚀 DevOps Study - Setup Environment"
echo "=========================================="

# Detectar SO
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

echo "📦 Instalando dependências base..."
cd gerar-insights
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

echo ""
echo "📦 Instalando dependências de desenvolvimento..."
$PYTHON_CMD -m pip install -r requirements-dev.txt

echo ""
echo "✅ Environment setup completo!"
echo ""
echo "Próximos passos:"
echo "  1. Rodar testes: python -m pytest tests/ -v"
echo "  2. Com cobertura: python -m pytest tests/ --cov=app"
echo "  3. Iniciar docker: docker-compose up -d"
echo ""

