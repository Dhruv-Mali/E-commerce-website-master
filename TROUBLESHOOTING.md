# Troubleshooting Guide

## Common Issues and Solutions

### 1. "Customer has no attribute" Error
**Symptom:** Error when accessing pages as authenticated user
```
AttributeError: 'User' object has no attribute 'customer'
```

**Solution:** This has been fixed! The app now automatically creates Customer profiles using `get_or_create()` with proper defaults.

**Manual Fix (if needed):**
```python
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from store.models import Customer
>>> for user in User.objects.all():
...     Customer.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email})
```

---

### 2. Missing Static Files
**Symptom:** CSS/JS not loading, broken images

**Solution:**
```bash
python manage.py collectstatic --noinput
```

---

### 3. Database Migration Issues
**Symptom:** Database errors, missing tables

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4. Stripe Payment Not Working
**Symptom:** Payment button doesn't redirect to Stripe

**Checklist:**
- [ ] Check `.env` file has valid Stripe keys
- [ ] Verify `STRIPE_SECRET_KEY` and `STRIPE_PUBLIC_KEY` are set
- [ ] Test with Stripe test card: `4242 4242 4242 4242`
- [ ] Check console for JavaScript errors

**Test Stripe Keys:**
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STRIPE_SECRET_KEY)
>>> print(settings.STRIPE_PUBLIC_KEY)
```

---

### 5. Cart Not Updating
**Symptom:** Items not adding to cart

**Solution:**
1. Check browser console for JavaScript errors
2. Verify CSRF token is present
3. Clear browser cookies
4. Hard refresh (Ctrl+F5)

---

### 6. Port Already in Use
**Symptom:** `Error: That port is already in use`

**Solution:**
```bash
# Use different port
python manage.py runserver 8080

# Or kill the process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### 7. Module Not Found Errors
**Symptom:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
pip install -r requirements.txt
```

---

### 8. SECRET_KEY Not Set
**Symptom:** `ImproperlyConfigured: The SECRET_KEY setting must not be empty`

**Solution:**
1. Check `.env` file exists in project root
2. Verify `SECRET_KEY` is set in `.env`
3. Restart the server

---

### 9. Images Not Displaying
**Symptom:** Broken image icons on product pages

**Possible Causes:**
1. Product has no image uploaded
2. Image file doesn't exist
3. MEDIA_URL not configured

**Solution:**
```bash
# Check media settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.MEDIA_URL)
>>> print(settings.MEDIA_ROOT)
```

---

### 10. Docker Build Fails
**Symptom:** Docker build errors

**Solution:**
```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## Quick Diagnostics

### Run System Check
```bash
python manage.py check
```

### Test Database Connection
```bash
python manage.py dbshell
```

### Verify Environment Variables
```bash
python manage.py shell
>>> import os
>>> print(os.environ.get('SECRET_KEY'))
>>> print(os.environ.get('DEBUG'))
```

### Check Installed Apps
```bash
python manage.py showmigrations
```

---

## Getting Help

If you encounter issues not covered here:

1. Check Django logs in console
2. Check browser console for JavaScript errors
3. Review `FIXES_APPLIED.md` for known issues
4. Check Django documentation: https://docs.djangoproject.com/
5. Open an issue on GitHub

---

## Useful Commands

```bash
# Create superuser
python manage.py createsuperuser

# Reset database (WARNING: Deletes all data)
del db.sqlite3
python manage.py migrate

# Load sample data
python scripts/populate_database.py

# Run tests
python manage.py test

# Check for security issues
python manage.py check --deploy
```

---

## Performance Tips

1. **Enable caching** for production
2. **Use CDN** for static files
3. **Optimize images** before uploading
4. **Enable GZIP** compression
5. **Use production WSGI server** (gunicorn)

---

## Security Checklist for Production

- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Regular security updates

---

**Last Updated:** 2024
