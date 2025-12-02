@echo off
echo ========================================
echo Pre-Migration Verification Script
echo ========================================
echo.

echo Checking critical files...
echo.

set ERROR=0

if exist "store\validators.py" (
    echo [OK] store\validators.py exists
) else (
    echo [ERROR] store\validators.py MISSING
    set ERROR=1
)

if exist "store\models_extended.py" (
    echo [OK] store\models_extended.py exists
) else (
    echo [ERROR] store\models_extended.py MISSING
    set ERROR=1
)

if exist "store\views_extended.py" (
    echo [OK] store\views_extended.py exists
) else (
    echo [ERROR] store\views_extended.py MISSING
    set ERROR=1
)

if exist "store\urls_extended.py" (
    echo [OK] store\urls_extended.py exists
) else (
    echo [ERROR] store\urls_extended.py MISSING
    set ERROR=1
)

if exist "store\admin_extended.py" (
    echo [OK] store\admin_extended.py exists
) else (
    echo [ERROR] store\admin_extended.py MISSING
    set ERROR=1
)

if exist "store\webhooks.py" (
    echo [OK] store\webhooks.py exists
) else (
    echo [ERROR] store\webhooks.py MISSING
    set ERROR=1
)

if exist "store\cache_utils.py" (
    echo [OK] store\cache_utils.py exists
) else (
    echo [ERROR] store\cache_utils.py MISSING
    set ERROR=1
)

if exist "static\js\cart_enhanced.js" (
    echo [OK] static\js\cart_enhanced.js exists
) else (
    echo [ERROR] static\js\cart_enhanced.js MISSING
    set ERROR=1
)

if exist "static\css\enhancements.css" (
    echo [OK] static\css\enhancements.css exists
) else (
    echo [ERROR] static\css\enhancements.css MISSING
    set ERROR=1
)

echo.
echo ========================================

if %ERROR%==0 (
    echo [SUCCESS] All critical files present!
    echo.
    echo You can now run:
    echo   python manage.py makemigrations
    echo   python manage.py migrate
    echo.
) else (
    echo [FAILED] Some files are missing!
    echo Please check the errors above.
    echo.
)

echo ========================================
pause
