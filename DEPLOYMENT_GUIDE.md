# 🚀 DEPLOYMENT & PRODUCTION SETUP GUIDE

## Pre-Deployment Checklist

### Security
- [ ] DEBUG = False
- [ ] SECRET_KEY = strong random (50+ chars)
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS/SSL enabled
- [ ] Database password changed
- [ ] Email credentials secured
- [ ] Payment keys in production mode
- [ ] Twilio credentials updated
- [ ] Security headers enabled
- [ ] CSRF protection enabled
- [ ] Rate limiting enabled

### Database
- [ ] Database created
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Backups configured
- [ ] Database optimized
- [ ] Indexes created

### Static Files
- [ ] Static files collected
- [ ] Media directory writable
- [ ] CDN configured (optional)
- [ ] Compression enabled

### Monitoring
- [ ] Error logging configured
- [ ] Performance monitoring setup
- [ ] Alerts configured
- [ ] Backup verification

---

## Step 1: Environment Setup

### 1.1 Generate Strong SECRET_KEY
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copy output to .env
```

### 1.2 Update .env File
```env
# Production settings
DEBUG=False
SECRET_KEY=your-generated-50-char-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=mysql
DB_NAME=ecommerce_prod
DB_USER=ecommerce_user
DB_PASSWORD=strong_password_here
DB_HOST=db.yourdomain.com
DB_PORT=3306

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Payment
STRIPE_PUBLIC_KEY=pk_live_your_key
STRIPE_SECRET_KEY=sk_live_your_key
RAZORPAY_KEY_ID=your_prod_key_id
RAZORPAY_KEY_SECRET=your_prod_key_secret

# Twilio
TWILIO_ACCOUNT_SID=your_prod_sid
TWILIO_AUTH_TOKEN=your_prod_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 1.3 Verify Settings
```bash
python manage.py check --deploy
```

---

## Step 2: Database Setup

### 2.1 Create Database
```bash
# MySQL
mysql -u root -p
CREATE DATABASE ecommerce_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON ecommerce_prod.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2.2 Apply Migrations
```bash
python manage.py migrate
```

### 2.3 Create Superuser
```bash
python manage.py createsuperuser
```

### 2.4 Load Sample Data (Optional)
```bash
python manage.py loaddata initial_data.json
```

### 2.5 Optimize Database
```bash
# Create indexes
python manage.py sqlsequencereset apps.store apps.loginsys | python manage.py dbshell

# Analyze tables
mysql -u ecommerce_user -p ecommerce_prod -e "ANALYZE TABLE store_product, store_order, store_customer;"
```

---

## Step 3: Static Files

### 3.1 Collect Static Files
```bash
python manage.py collectstatic --no-input
```

### 3.2 Verify Collection
```bash
ls -la staticfiles/
```

### 3.3 Configure Web Server
```nginx
# nginx.conf
location /static/ {
    alias /path/to/staticfiles/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}

location /media/ {
    alias /path/to/media/;
    expires 7d;
}
```

---

## Step 4: Web Server Setup

### 4.1 Install Gunicorn
```bash
pip install gunicorn
```

### 4.2 Create Gunicorn Service
```bash
# /etc/systemd/system/gunicorn.service
[Unit]
Description=Gunicorn application server
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind unix:/run/gunicorn.sock \
    --timeout 60 \
    config.ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4.3 Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### 4.4 Configure Nginx
```bash
# /etc/nginx/sites-available/ecommerce
upstream gunicorn {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/ecommerce_access.log;
    error_log /var/log/nginx/ecommerce_error.log;
    
    # Client upload size
    client_max_body_size 10M;
    
    # Static files
    location /static/ {
        alias /path/to/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /path/to/media/;
        expires 7d;
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 4.5 Enable Nginx Site
```bash
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 5: SSL/HTTPS Setup

### 5.1 Install Certbot
```bash
sudo apt-get install certbot python3-certbot-nginx
```

### 5.2 Generate Certificate
```bash
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 5.3 Auto-Renewal
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Step 6: Database Backups

### 6.1 Create Backup Script
```bash
#!/bin/bash
# /usr/local/bin/backup_ecommerce.sh

BACKUP_DIR="/backups/ecommerce"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="ecommerce_prod"
DB_USER="ecommerce_user"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /path/to/media/

# Keep only last 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### 6.2 Schedule Backup
```bash
# Add to crontab
0 2 * * * /usr/local/bin/backup_ecommerce.sh
```

### 6.3 Test Restore
```bash
# Test restore process monthly
gunzip < backup.sql.gz | mysql -u user -p database
```

---

## Step 7: Monitoring & Logging

### 7.1 Configure Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/ecommerce/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/ecommerce/errors.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

### 7.2 Monitor Logs
```bash
# Real-time log monitoring
tail -f /var/log/ecommerce/django.log

# Search for errors
grep ERROR /var/log/ecommerce/django.log

# Count errors
grep ERROR /var/log/ecommerce/django.log | wc -l
```

### 7.3 Set Up Alerts
```bash
# Monitor disk space
df -h | grep -E '^/dev'

# Monitor memory
free -h

# Monitor CPU
top -b -n 1 | head -20
```

---

## Step 8: Performance Optimization

### 8.1 Enable Caching
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 8.2 Database Optimization
```bash
# Analyze query performance
EXPLAIN SELECT * FROM store_product WHERE category = 'Electronics';

# Create indexes
ALTER TABLE store_product ADD INDEX idx_category (category);
ALTER TABLE store_order ADD INDEX idx_customer (customer_id);
```

### 8.3 Compression
```nginx
# Enable gzip compression
gzip on;
gzip_types text/plain text/css text/javascript application/json;
gzip_min_length 1000;
```

---

## Step 9: Security Hardening

### 9.1 Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3306/tcp  # MySQL (internal only)
```

### 9.2 SSH Security
```bash
# Disable root login
sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Change SSH port
sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config

# Restart SSH
sudo systemctl restart sshd
```

### 9.3 Fail2Ban
```bash
# Install
sudo apt-get install fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Enable
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## Step 10: Monitoring & Maintenance

### 10.1 Health Check
```bash
#!/bin/bash
# /usr/local/bin/health_check.sh

# Check Django
curl -s http://localhost/health/ | grep -q "ok" || echo "Django down"

# Check Database
mysql -u user -p -e "SELECT 1" > /dev/null 2>&1 || echo "Database down"

# Check Disk
DISK=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK -gt 90 ]; then
    echo "Disk usage critical: $DISK%"
fi

# Check Memory
MEM=$(free | awk 'NR==2 {print int($3/$2 * 100)}')
if [ $MEM -gt 90 ]; then
    echo "Memory usage critical: $MEM%"
fi
```

### 10.2 Schedule Health Check
```bash
# Add to crontab
*/5 * * * * /usr/local/bin/health_check.sh
```

### 10.3 Regular Maintenance
```bash
# Weekly
- Review error logs
- Check disk space
- Verify backups

# Monthly
- Update packages
- Review security logs
- Test backup restoration

# Quarterly
- Security audit
- Performance review
- Capacity planning
```

---

## Docker Deployment

### 10.1 Build Docker Image
```bash
docker build -t ecommerce:latest .
```

### 10.2 Run with Docker Compose
```bash
docker-compose up -d
```

### 10.3 Initialize Database
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 10.4 Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

---

## Troubleshooting

### Issue: 502 Bad Gateway
```bash
# Check Gunicorn
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50

# Check socket
ls -la /run/gunicorn.sock
```

### Issue: Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --no-input

# Check permissions
ls -la staticfiles/
chmod -R 755 staticfiles/
```

### Issue: Database Connection Error
```bash
# Check MySQL
sudo systemctl status mysql
mysql -u user -p -e "SELECT 1"

# Check credentials in .env
cat .env | grep DB_
```

### Issue: Email Not Sending
```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

---

## Rollback Procedure

### If Deployment Fails
```bash
# Stop services
sudo systemctl stop gunicorn
sudo systemctl stop nginx

# Restore previous version
git checkout previous_commit
python manage.py migrate --fake-initial

# Restore database backup
gunzip < backup.sql.gz | mysql -u user -p database

# Start services
sudo systemctl start gunicorn
sudo systemctl start nginx
```

---

## Performance Benchmarks

### Target Metrics
- Page load time: < 2 seconds
- API response: < 500ms
- Database query: < 100ms
- Uptime: 99.9%
- Error rate: < 0.1%

### Monitoring Tools
- New Relic
- Datadog
- Sentry
- CloudWatch
- Prometheus

---

## Support & Documentation

- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/
- Let's Encrypt: https://letsencrypt.org/
- MySQL: https://dev.mysql.com/
