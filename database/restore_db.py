#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MySQL Database Restore Script"""
import os
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def restore_database(backup_file):
    from dotenv import load_dotenv
    load_dotenv()
    
    db_name = os.getenv('DB_NAME', 'ecommerce_db')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    
    if not os.path.exists(backup_file):
        print(f"Backup file not found: {backup_file}")
        return False
    
    print(f"Restoring database: {db_name}")
    print(f"From file: {backup_file}")
    
    cmd = f'mysql -u {db_user} -p{db_password} {db_name} < {backup_file}'
    
    try:
        os.system(cmd)
        print("Restore completed successfully")
        return True
    except Exception as e:
        print(f"Restore failed: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python restore_db.py <backup_file>")
        sys.exit(1)
    
    restore_database(sys.argv[1])
