#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting AdVision Backend Build..."

# Print Python version
echo "📦 Python version:"
python --version

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements_prod.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!"
echo "🎉 AdVision Backend is ready to deploy!"