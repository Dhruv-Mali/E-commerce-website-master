# Database Management

## MySQL Database Folder

This folder contains database backup and restore scripts.

### Backup Database

```bash
python database/backup_db.py
```

Creates backup file: `database/backup_YYYYMMDD_HHMMSS.sql`

### Restore Database

```bash
python database/restore_db.py database/backup_20240130_120000.sql
```

### Manual Backup (Command Line)

```bash
mysqldump -u root -p ecommerce_db > database/manual_backup.sql
```

### Manual Restore (Command Line)

```bash
mysql -u root -p ecommerce_db < database/manual_backup.sql
```

### Database Configuration

Database settings are in `.env` file:
- DB_NAME=ecommerce_db
- DB_USER=root
- DB_PASSWORD=your_password
- DB_HOST=localhost
- DB_PORT=3306

### Backup Files

Backup files are stored in this folder with timestamp:
- `backup_20240130_120000.sql`
- `backup_20240131_150000.sql`

**Note:** Add `*.sql` to `.gitignore` to avoid committing large backup files.
