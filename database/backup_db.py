#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MySQL Database Backup Script"""
import os
import sys
import subprocess
from datetime import datetime

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def backup_database():
    from dotenv import load_dotenv
    load_dotenv()
    
    db_name = os.getenv('DB_NAME', 'ecommerce_db')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'database/backup_{timestamp}.sql'
    
    print(f"Backing up database: {db_name}")
    print(f"Backup file: {backup_file}")
    
    cmd = f'mysqldump -u {db_user} -p{db_password} {db_name} > {backup_file}'
    
    try:
        os.system(cmd)
        print(f"Backup completed: {backup_file}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

if __name__ == '__main__':
    backup_database()
