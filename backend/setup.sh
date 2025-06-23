#!/bin/bash

echo "📦 Creating virtual environment..."
python -m venv venv

echo "🐍 Activating virtual environment..."
source venv/Scripts/activate || source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "⚙️ Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🔐 Creating default roles..."
python manage.py init_roles

echo "🌱 Seeding the database with patients..."
python manage.py seed_patients

echo "🚀 All done. You can now run the server using:"
echo "    python manage.py runserver"
