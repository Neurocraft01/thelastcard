# Production Deployment Script
# The Last Card NFC Platform

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "The Last Card - Production Deployment" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Environment Check
Write-Host "Step 1: Checking Environment Variables..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found! Please create it from .env.example" -ForegroundColor Red
    exit 1
}

# Check if DEBUG is False
$envContent = Get-Content .env -Raw
if ($envContent -match "DEBUG=True") {
    Write-Host "WARNING: DEBUG is set to True! Change it to False for production." -ForegroundColor Red
    $response = Read-Host "Continue anyway? (yes/no)"
    if ($response -ne "yes") {
        exit 1
    }
}

Write-Host "✓ Environment file found" -ForegroundColor Green

# Step 2: Database Backup
Write-Host "`nStep 2: Creating Database Backup..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "backup_$timestamp.json"

python manage.py dumpdata --natural-foreign --natural-primary --indent 2 > $backupFile
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database backup created: $backupFile" -ForegroundColor Green
} else {
    Write-Host "ERROR: Database backup failed!" -ForegroundColor Red
    exit 1
}

# Step 3: Install Dependencies
Write-Host "`nStep 3: Installing Dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --upgrade
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "ERROR: Dependency installation failed!" -ForegroundColor Red
    exit 1
}

# Step 4: Database Migrations
Write-Host "`nStep 4: Running Database Migrations..." -ForegroundColor Yellow
python manage.py migrate --no-input
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Migrations applied successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Migration failed!" -ForegroundColor Red
    Write-Host "Attempting to restore backup..." -ForegroundColor Yellow
    # Restore logic would go here if using PostgreSQL
    exit 1
}

# Step 5: Collect Static Files
Write-Host "`nStep 5: Collecting Static Files..." -ForegroundColor Yellow
python manage.py collectstatic --no-input --clear
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Static files collected" -ForegroundColor Green
} else {
    Write-Host "ERROR: Static file collection failed!" -ForegroundColor Red
    exit 1
}

# Step 6: Run Deployment Checks
Write-Host "`nStep 6: Running Django Deployment Checks..." -ForegroundColor Yellow
python manage.py check --deploy
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Deployment checks passed" -ForegroundColor Green
} else {
    Write-Host "WARNING: Some deployment checks failed. Review the output above." -ForegroundColor Yellow
    $response = Read-Host "Continue with deployment? (yes/no)"
    if ($response -ne "yes") {
        exit 1
    }
}

# Step 7: Test Email Configuration
Write-Host "`nStep 7: Testing Email Configuration..." -ForegroundColor Yellow
$emailTest = @"
from django.core.mail import send_mail
from django.conf import settings
try:
    send_mail(
        'Production Deployment Test',
        'This is a test email from your NFC platform production deployment.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
"@

$emailResult = python manage.py shell -c $emailTest
if ($emailResult -match "SUCCESS") {
    Write-Host "✓ Email configuration working" -ForegroundColor Green
} else {
    Write-Host "WARNING: Email test failed. Check your SMTP settings." -ForegroundColor Yellow
    Write-Host $emailResult -ForegroundColor Red
}

# Step 8: Create Superuser (if needed)
Write-Host "`nStep 8: Superuser Account..." -ForegroundColor Yellow
$createSuperuser = Read-Host "Do you want to create a superuser account? (yes/no)"
if ($createSuperuser -eq "yes") {
    python manage.py createsuperuser
}

# Step 9: Final Security Checklist
Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "Pre-Deployment Security Checklist" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$checklist = @(
    "DEBUG=False in production .env",
    "SECRET_KEY is unique (50+ characters)",
    "ALLOWED_HOSTS includes your domain",
    "Database is PostgreSQL (not SQLite)",
    "SSL certificate is active",
    "Email SMTP credentials are correct",
    "Static files are served correctly",
    "Media files storage is configured",
    "Backup system is in place",
    "Monitoring/error tracking is set up"
)

foreach ($item in $checklist) {
    Write-Host "  [ ] $item" -ForegroundColor White
}

# Step 10: Deployment Summary
Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "Deployment Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✓ Environment verified" -ForegroundColor Green
Write-Host "✓ Database backup created: $backupFile" -ForegroundColor Green
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host "✓ Migrations applied" -ForegroundColor Green
Write-Host "✓ Static files collected" -ForegroundColor Green
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review the security checklist above" -ForegroundColor White
Write-Host "2. Test the application thoroughly" -ForegroundColor White
Write-Host "3. Monitor error logs after going live" -ForegroundColor White
Write-Host "4. Have rollback plan ready" -ForegroundColor White
Write-Host ""

Write-Host "To start the production server:" -ForegroundColor Yellow
Write-Host "  gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:8000 --workers 4" -ForegroundColor Cyan
Write-Host ""

Write-Host "Deployment preparation complete! 🚀" -ForegroundColor Green
Write-Host ""

# Ask if user wants to start the server
$startServer = Read-Host "Would you like to start the production server now? (yes/no)"
if ($startServer -eq "yes") {
    Write-Host "`nStarting production server..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    
    # Start gunicorn
    gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:8000 --workers 4 --log-level info
}
