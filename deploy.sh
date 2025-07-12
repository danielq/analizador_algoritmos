#!/bin/bash

echo "🚀 Desplegando Analizador de Algoritmos..."

# Verificar que existe el token
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN no está configurado"
    echo "Por favor, ejecuta: export TELEGRAM_BOT_TOKEN='tu_token_aqui'"
    exit 1
fi

# Opciones de despliegue
echo "Selecciona tu opción de despliegue:"
echo "1) Railway (Recomendado - Gratis)"
echo "2) Heroku"
echo "3) Docker local"
echo "4) VPS con Docker"

read -p "Opción (1-4): " choice

case $choice in
    1)
        echo "📦 Desplegando en Railway..."
        # Instalar Railway CLI si no está instalado
        if ! command -v railway &> /dev/null; then
            echo "Instalando Railway CLI..."
            npm install -g @railway/cli
        fi
        
        # Login y deploy
        railway login
        railway init
        railway up
        ;;
    2)
        echo "📦 Desplegando en Heroku..."
        # Verificar si Heroku CLI está instalado
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI no está instalado"
            echo "Instala desde: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        # Crear app y deploy
        heroku create analizador-algoritmos-$(date +%s)
        heroku config:set TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
        git push heroku main
        ;;
    3)
        echo "🐳 Desplegando con Docker local..."
        docker-compose up -d
        echo "✅ Bot ejecutándose en Docker"
        echo "Para ver logs: docker-compose logs -f"
        ;;
    4)
        echo "🖥️  Desplegando en VPS..."
        echo "1. Sube el código a tu VPS"
        echo "2. Instala Docker: curl -fsSL https://get.docker.com | sh"
        echo "3. Ejecuta: docker-compose up -d"
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo "✅ ¡Despliegue completado!" 