set -euo pipefail

echo "Devcontainer ready. Tool versions:"
node -v
npm -v
mysql --version || true

echo
echo "Waiting for MySQL to accept connections on localhost:3306..."
for i in {1..60}; do
  if mysqladmin ping -h 127.0.0.1 -uroot -ppassword --silent > /dev/null 2>&1; then
    echo "MySQL is up. Database: data-analysis (user: root / password: password)"
    exit 0
  fi
  sleep 1
done

echo "MySQL did not become ready in time. Check the db container logs." >&2
exit 1