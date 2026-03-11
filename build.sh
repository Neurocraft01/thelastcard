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
import os, sys
try:
    import psycopg2
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        print("DATABASE_URL is not set — skipping connection check.")
        sys.exit(0)
    conn = psycopg2.connect(url, connect_timeout=10)
    conn.close()
    print("Database connection: OK")
except Exception as e:
    print(f"\n[BUILD ERROR] Cannot connect to the database: {e}")
    print("Ensure DATABASE_URL in Render points to the Supabase SESSION POOLER URL:")
    print("  postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres")
    print("NOT the direct host (db.[ref].supabase.co) which is IPv6-only.")
    sys.exit(1)
EOF

# Run database migrations
python manage.py migrate --no-input

echo "Build completed successfully!"
