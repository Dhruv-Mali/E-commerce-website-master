"""
migrate_to_docker.py
--------------------
Migrates local SQLite data into the Docker MySQL container.
Handles: emoji encoding, duplicate customers, MySQL readiness timing.
"""

import os
import sys
import json
import subprocess
import time

os.environ["PYTHONUTF8"] = "1"

PROJECT = os.path.dirname(os.path.abspath(__file__))
DUMP_FILE = os.path.join(PROJECT, "datadump.json")

DB_HOST     = "127.0.0.1"
DB_PORT     = 3307
DB_NAME     = "ecommerce_db"
DB_USER     = "ecommerce_user"
DB_PASSWORD = "Dhruv@10"


def run(cmd, desc, env=None, check=True):
    print(f"\n[+] {desc}")
    print(f"    $ {cmd}")
    r = subprocess.run(cmd, shell=True, cwd=PROJECT, env=env or os.environ.copy())
    if check and r.returncode != 0:
        print(f"\n[!] FAILED: {desc}")
        sys.exit(1)
    print("    Done.")
    return r.returncode


def clean_dump(path):
    """
    Remove duplicate Customer objects (same user_id) from the dump.
    Keeps the first occurrence of each user_id.
    This prevents IntegrityError on store_customer.user_id unique constraint.
    """
    print("\n[+] Cleaning dump: removing duplicate Customer records...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen_user_ids = set()
    cleaned = []
    removed = 0
    for obj in data:
        if obj.get("model") == "store.customer":
            uid = obj["fields"].get("user")
            if uid is not None:
                uid = tuple(uid) if isinstance(uid, list) else uid  # lists aren't hashable
                if uid in seen_user_ids:
                    removed += 1
                    continue
                seen_user_ids.add(uid)
        cleaned.append(obj)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"    Removed {removed} duplicate Customer record(s). Kept {len(cleaned)} objects total.")


def wait_for_mysql_ready(timeout=180):
    """Try connecting with pymysql + running SELECT 1. Retries until truly ready."""
    try:
        import pymysql
    except ImportError:
        print("[!] pymysql not installed. Run: pip install pymysql")
        sys.exit(1)

    print(f"\n⏳ Waiting for MySQL at {DB_HOST}:{DB_PORT} to be fully ready...")
    start = time.time()
    attempt = 0
    while True:
        attempt += 1
        try:
            conn = pymysql.connect(
                host=DB_HOST, port=DB_PORT,
                user=DB_USER, password=DB_PASSWORD,
                database=DB_NAME, connect_timeout=3,
            )
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
            conn.close()
            elapsed = int(time.time() - start)
            print(f"\n    ✅ MySQL ready! ({elapsed}s, {attempt} attempts)")
            return
        except Exception as e:
            elapsed = int(time.time() - start)
            if elapsed > timeout:
                print(f"\n[!] MySQL not ready after {timeout}s. Error: {e}")
                print("    Run: docker logs ecommerce-mysql")
                sys.exit(1)
            print(f"    Attempt {attempt}: waiting... ({elapsed}s)          ", end="\r")
            time.sleep(3)


if __name__ == "__main__":
    print("=" * 60)
    print("  SQLite → Docker MySQL Migration")
    print("=" * 60)

    # ── Step 1: Export SQLite data ────────────────────────────────
    run(
        "python manage.py dumpdata --natural-foreign --natural-primary "
        "-e contenttypes -e auth.Permission -e admin.logentry "
        "-e sessions.session -o datadump.json",
        "Exporting SQLite → datadump.json"
    )

    # ── Step 2: Clean duplicate customers from dump ───────────────
    clean_dump(DUMP_FILE)

    # ── Step 3: Start ONLY MySQL ──────────────────────────────────
    run("docker-compose up -d mysql", "Starting MySQL container only")

    # ── Step 4: Wait until MySQL accepts real queries ─────────────
    wait_for_mysql_ready(timeout=180)

    # ── Step 5: Build env for local Django → Docker MySQL ─────────
    env = os.environ.copy()
    env.update({
        "DB_ENGINE":    "mysql",
        "DB_HOST":      DB_HOST,
        "DB_PORT":      str(DB_PORT),
        "DB_NAME":      DB_NAME,
        "DB_USER":      DB_USER,
        "DB_PASSWORD":  DB_PASSWORD,
        "PYTHONUTF8":   "1",
    })

    # ── Step 6: Run migrations to create tables ───────────────────
    run("python manage.py migrate --run-syncdb", "Creating tables in Docker MySQL", env=env)

    # ── Step 7: Load data ─────────────────────────────────────────
    print("\n[+] Loading data into Docker MySQL (127.0.0.1:3307)")
    r = subprocess.run(
        "python manage.py loaddata datadump.json",
        shell=True, cwd=PROJECT, env=env
    )
    if r.returncode != 0:
        print("[!] loaddata failed. See error above.")
        sys.exit(1)
    print("    ✅ All data loaded successfully!")

    # ── Step 8: Bring up the full stack ───────────────────────────
    run("docker-compose up -d --build", "Starting full stack (web + redis + mysql)")

    print("\n" + "=" * 60)
    print("  ✅  Migration complete!")
    print("=" * 60)

    # Verify
    print("\nVerifying product count in Docker MySQL:")
    subprocess.run(
        f'docker exec ecommerce-mysql mysql -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} '
        f'-e "SELECT COUNT(*) AS products FROM store_product; '
        f'SELECT COUNT(*) AS customers FROM store_customer; '
        f'SELECT COUNT(*) AS users FROM auth_user;"',
        shell=True
    )
