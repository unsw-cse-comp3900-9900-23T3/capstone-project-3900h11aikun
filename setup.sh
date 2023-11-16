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
    echo "follow the instruction show below"
    echo ""
    echo "1. You can run \"npx http-server frontend -c 1 -p 6081\" inside capstone-project-3900h11aikun directory now"
    echo ""
    echo "If the terminal ask you to install http-server then select yes"
    echo ""
    echo "copy the FIRST LINK shown under \"Available on:\" to your google browser, then DO NEXT STEP. "
    echo ""
    echo "2. open another terminal (don't close current running frontend terminal) and cd to \"capstone-project-3900h11aikun/backend\" folder"
    echo ""
    echo "enter \"python3 app.py\"if using linux/macos, enter \"python app.py\" if using windows"
    echo ""
    echo "** If your terminal shows ImportError: cannot import name EVENT_ TYPE_OPENED from 'watchdog.events'... "
    echo "Try \"pip install --upgrade watchdog\""
    echo ""
    echo "**If no error shows, you can use the website now"
else
    echo "Node.js is not installed. Please install Node.js package. After installing successful, run ./setup.sh again"
fi