DB_NAME="db.sqlite3"

echo "Dropping the database..."
if [ -f $DB_NAME ]; then
    rm -f $DB_NAME
    echo "Database $DB_NAME dropped successfully."
else
    echo "Database $DB_NAME does not exist."
fi

echo "Creating the database..."

echo "Running migrations..."
pdm migrate

echo "Populating the database..."
pdm run populate --all

echo "Database reset and populated successfully!"
