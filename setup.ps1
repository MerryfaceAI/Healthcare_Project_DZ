Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Applying migrations..." -ForegroundColor Cyan
python manage.py makemigrations
python manage.py migrate

Write-Host "Creating default roles..." -ForegroundColor Cyan
python manage.py init_roles

Write-Host "Seeding the database with fake patients..." -ForegroundColor Cyan
python manage.py seed_patients

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Start the server with: python manage.py runserver" -ForegroundColor Yellow
