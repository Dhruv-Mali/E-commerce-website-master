#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick start script"""
import os
import sys
import subprocess

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def main():
    print("\n" + "="*60)
    print("STARTING E-COMMERCE PROJECT")
    print("="*60)
    
    print("\nServer starting at: http://127.0.0.1:8000/")
    print("Admin panel: http://127.0.0.1:8000/admin/")
    print("Store: http://127.0.0.1:8000/store/")
    print("\nPress CTRL+C to stop\n")
    
    subprocess.run([sys.executable, 'manage.py', 'runserver'])

if __name__ == '__main__':
    main()
