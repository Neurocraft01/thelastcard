#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Validate DB connectivity before attempting migrations.
# Render free tier is IPv4-only. The DATABASE_URL MUST point to the Supabase
# session-pooler host (aws-0-[region].pooler.supabase.com, port 6543) which
# resolves over IPv4.  The direct host (db.[ref].supabase.co) uses IPv6 and
# will fail here.  If you see a "Network is unreachable" error below, go to:
#   Render Dashboard → your service → Environment → DATABASE_URL
# and set it to your Supabase *session pooler* connection string:
#   postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
python - <<'EOF'
import os, sys, re
url = os.environ.get("DATABASE_URL", "")
if not url:
    print("DATABASE_URL is not set — skipping connection check.")
    sys.exit(0)

# Reject direct Supabase host (db.[ref].supabase.co) — IPv6-only, unreachable on Render
if re.search(r'db\.[a-z]+\.supabase\.co', url):
    print("\n[BUILD ERROR] DATABASE_URL is pointing to the Supabase DIRECT connection host.")
    print("  Detected host pattern: db.[ref].supabase.co")
    print("  This resolves to an IPv6 address and is unreachable on Render's free/starter tier.")
    print()
    print("  ACTION REQUIRED — In the Render dashboard:")
    print("    Service → Environment → DATABASE_URL")
    print("  Set it to your Supabase SESSION POOLER URL (IPv4, port 6543):")
    print("    postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require")
    print()
    print("  Find this URL in: Supabase Dashboard → Settings → Database → Connection string")
    print("  Select mode: 'Session' and copy the URI.")
    sys.exit(1)

try:
    import psycopg2
    conn = psycopg2.connect(url, connect_timeout=10)
    conn.close()
    print("Database connection: OK")
except Exception as e:
    print(f"\n[BUILD ERROR] Cannot connect to the database: {e}")
    print("Ensure DATABASE_URL in Render points to the Supabase SESSION POOLER URL:")
    print("  postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require")
    print("NOT the direct host (db.[ref].supabase.co) which is IPv6-only.")
    sys.exit(1)
EOF

# Run database migrations
python manage.py migrate --no-input

echo "Build completed successfully!"
