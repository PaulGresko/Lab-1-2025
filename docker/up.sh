docker compose up -d

echo "Waiting for ClickHouse to be ready..."

# Ждём, пока ClickHouse начнет отвечать
until docker exec clickhouse clickhouse-client --query="SELECT 1" &> /dev/null
do
    echo "Still waiting..."
    sleep 1
done

echo "Running SQL init script..."
docker exec -i clickhouse clickhouse-client < ./init/create_tables.sql

echo "Database initialization completed."