@echo off
echo ========================================
echo E-Commerce Improvements - Setup Script
echo ========================================
echo.

echo Step 1: Creating migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ERROR: Migration creation failed!
    pause
    exit /b 1
)
echo ✓ Migrations created successfully
echo.

echo Step 2: Applying migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)
echo ✓ Migrations applied successfully
echo.

echo Step 3: Collecting static files...
python manage.py collectstatic --noinput
echo ✓ Static files collected
echo.

echo ========================================
echo ✓ ALL IMPROVEMENTS APPLIED SUCCESSFULLY!
echo ========================================
echo.
echo Next steps:
echo 1. Update your templates (see QUICK_START_GUIDE.md)
echo 2. Configure Stripe webhooks
echo 3. Test new features
echo 4. Review IMPROVEMENTS_APPLIED.md for details
echo.
pause
