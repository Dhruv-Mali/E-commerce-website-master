#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix common errors in the project"""
import os
import sys
import subprocess

# Fix Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def run_check(description, command):
    print(f"\n{'='*60}")
    print(f">> {description}")
    print(f"{'='*60}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("PASSED")
        return True
    else:
        print("FAILED")
        if result.stderr:
            print(result.stderr)
        return False

def main():
    print("\n" + "="*60)
    print("CHECKING FOR ERRORS")
    print("="*60)
    
    checks = [
        ("Django System Check", "python manage.py check"),
        ("Check Migrations", "python manage.py showmigrations"),
    ]
    
    passed = 0
    failed = 0
    
    for desc, cmd in checks:
        if run_check(desc, cmd):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\nNo errors found! Project is ready.")
        print("\nRun: python manage.py runserver")
    else:
        print("\nSome checks failed. Review errors above.")
    
    return failed == 0

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
