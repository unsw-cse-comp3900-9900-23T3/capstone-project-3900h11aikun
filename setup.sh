# by run this, database will be changed to default database, all changes made will be deleted including register a new user and so on
if [ -f "./backend/database.db" ]; then
    rm "./backend/database.db"
fi

if [ ! -f "./backend/default_database.db" ]; then
    cp ./backend/db/default_database.db ./backend
fi

mv ./backend/default_database.db ./backend/database.db

if [ ! -d "./backend/uploads" ]; then
    mkdir backend/uploads;
fi

OS=$(uname -s)

case "$OS" in
  Linux*)     
    echo "Installing requirements on Linux..."
    pip3 install -r backend/requirements.txt > /dev/null 2>&1
    ;;
  Darwin*)    
    echo "Installing requirements on macOS..."
    pip3 install -r backend/requirements.txt > /dev/null 2>&1
    ;; 
  *)          
    echo "Installing requirements on windows or other OS..."
    pip install -r backend/requirements.txt > /dev/null 2>&1
    ;;
esac
echo ""
node --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Node.js is already installed."
    echo ""
    echo "You can run \"npx http-server frontend -c 1 -p 6081\" inside capstone-project-3900h11aikun directory now"
else
    echo "Node.js is not installed. Please install Node.js package. After installing successful, run ./setup.sh again"
fi