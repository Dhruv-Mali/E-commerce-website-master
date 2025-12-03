# 🗄️ MySQL Database Setup Guide

## Prerequisites

1. **Install MySQL Server**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Or install via XAMPP/WAMP which includes MySQL
   - Make sure MySQL service is running

2. **Verify MySQL Installation**
   ```bash
   mysql --version
   ```

## Step-by-Step Setup

### 1. Update Environment Variables

Edit the `.env` file in your project root and update these values:

```env
# MySQL Database Configuration
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

**Important:** Replace `your_actual_mysql_password` with your actual MySQL root password.

### 2. Create Database (Option A - Automatic)

Run the automated setup script:

```bash
python setup_mysql.py
```

This script will:
- Create the database if it doesn't exist
- Test the connection
- Show you next steps

### 3. Create Database (Option B - Manual)

If you prefer manual setup:

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional, for security)
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

### 4. Run Django Migrations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python create_admin.py
```

### 6. Populate Sample Data

```bash
python utils\scripts\populate_database.py
```

### 7. Start Development Server

```bash
python manage.py runserver
```

## Troubleshooting

### Common Issues

**1. "Access denied for user 'root'@'localhost'"**
- Check your MySQL password in `.env` file
- Make sure MySQL service is running

**2. "Can't connect to MySQL server"**
- Verify MySQL is installed and running
- Check host and port in `.env` file

**3. "Database doesn't exist"**
- Run `python setup_mysql.py` to create it automatically
- Or create manually using MySQL command line

**4. "No module named 'MySQLdb'"**
- Install MySQL client: `pip install mysqlclient`
- On Windows, you might need Visual Studio Build Tools

### MySQL Service Commands (Windows)

```bash
# Start MySQL service
net start mysql

# Stop MySQL service
net stop mysql

# Check if MySQL is running
sc query mysql
```

### Verify Database Connection

```bash
# Test Django database connection
python manage.py dbshell
```

## Database Configuration Details

The project is configured to use:
- **Engine:** MySQL
- **Character Set:** utf8mb4 (supports emojis and international characters)
- **Collation:** utf8mb4_unicode_ci
- **Connection Options:** Strict mode enabled for data integrity

## Security Notes

1. **Never commit passwords** to version control
2. **Use strong passwords** for production
3. **Create dedicated database users** instead of using root
4. **Enable SSL** for production databases
5. **Regular backups** are recommended

## Production Considerations

For production deployment:

```env
# Production settings
DEBUG=False
DB_HOST=your_production_host
DB_PASSWORD=strong_production_password
```

Additional security settings in `settings.py` will be automatically enabled when `DEBUG=False`.

---

## Quick Commands Reference

```bash
# Setup everything
python setup_mysql.py
python manage.py migrate
python create_admin.py
python utils\scripts\populate_database.py
python manage.py runserver

# Access application
http://127.0.0.1:8000/

# Access admin panel
http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
```

---

**Need help?** Check the main README.md or open an issue in the repository.