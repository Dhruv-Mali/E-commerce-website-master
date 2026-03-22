# Database Management

## Overview

This folder contains database backup and restore scripts. The project supports both **SQLite** (default) and **MySQL** databases.

### Switching Databases

Set `DB_ENGINE` in your `.env` file:
```env
# SQLite (default - no extra setup needed)
DB_ENGINE=sqlite3

# MySQL (requires MySQL 8.0+ server)
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

---

## Backup Database

### Using Script (MySQL)
```bash
python database/backup_db.py
```

Creates backup file: `database/backup_YYYYMMDD_HHMMSS.sql`

### Using Django (SQLite or MySQL)
```bash
python manage.py dumpdata > database/backup.json
```

### Manual Backup (MySQL)
```bash
mysqldump -u root -p ecommerce_db > database/manual_backup.sql
```

---

## Restore Database

### Using Script (MySQL)
```bash
python database/restore_db.py database/backup_20240130_120000.sql
```

### Using Django (SQLite or MySQL)
```bash
python manage.py loaddata database/backup.json
```

### Manual Restore (MySQL)
```bash
mysql -u root -p ecommerce_db < database/manual_backup.sql
```

---

## Database Configuration

Database settings are in the `.env` file in the project root. See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for detailed database setup instructions.

## Backup Files

Backup files are stored in this folder with timestamp:
- `backup_20240130_120000.sql`

**Note:** Add `*.sql` and `*.json` to `.gitignore` to avoid committing large backup files.
