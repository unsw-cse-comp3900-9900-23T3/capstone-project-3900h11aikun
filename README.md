# Student Industry Capstone Project Management System

## Download the code

The project repository is on the [github link here](https://github.com/unsw-cse-comp3900-9900-23T3/capstone-project-3900h11aikun). You can either `git clone` the code, or download the code in a zip file.

```
git clone git@github.com:unsw-cse-comp3900-9900-23T3/capstone-project-3900h11aikun.git
```
## Quick version to finish set up (See pictures of each step in section4 of final report if you need)
(Suppose using macOs or linux system and node.js, python3, pip already installed, if not see set up instructions below) 
If setup successfully you can skip below frontend setup and start backend section

Run `chmod +x setup.sh` first, then run `./setup.sh` in root directory (...../capstone-project-3900h11aikun).

Run “npx http-server frontend -c 1 -p 6081” in the root directory.

Open another terminal and cd to the backend folder folder(...../capstone-project-3900h11aikun/backend) and run `python3 app.py`.

If you are using school account you may see ImportError: cannot import name EVENT_ TYPE_OPENED from 'watchdog.events'... 
Try to run `pip install --upgrade watchdog` and run `python3 app.py` again, the issue should be solved.

Copy the FIRST LINK under “Available on” to Chrome browser. Do not use the second link.


## Steps to set up front end
Please ensure you have `Node.js` and `npm` installed on your computer. You can check this by running the following commands in any termina:

```bash
node -v        
npm -v
```
If you do not have `Node.js` and `npm` installed, visit [Node.js website](https://nodejs.org/en) to download them.

You can run `npx http-server frontend -c 1 -p 6081` in the root directory (...../capstone-project-3900h11aikun) now.

Copy the FIRST LINK under “Available on” to Chrome browser,do not use the second link. 
Then you can see our website now, but it can't work properly right now, start backend described below before use it.

## Steps to Start the Backend

Please ensure you have `python` and `pip` installed on your computer. You can check this by running the following commands in any termina:

```bash
python --version        # if you are on windows
python3 --version       # if you are on mac or linux

pip --version           # if you are on windows
pip3 --version          # if you are on mac or linux
```

If you do not have `python` or `pip` installed,
* for windows, please visit the [python download page](https://www.python.org/downloads/) to download the python. A version that is greater or equal to 3.9 is preferred. Make sure you click `Add to PATH` when installing python.
* for mac or linux, please open a terminal and run the following commands to install python and pip:

    ```bash
    sudo apt-get install python3
    sudo apt-get install python3-pip
    ```
    And then you can run the `python3 --version` and `pip3 --version` to check if the installation is successful.

Open the terminal in the capstone-project-3900h11aikun folder, and run the following commands:

```bash
# first move into the backend folder
cd backend

# install the requirements.txt file (only need to do this once)
pip install -r requirements.txt     # if you are on windows
pip3 install -r requirements.txt    # if you are on mac or linux

# run the backend server
python app.py                       # if you are on windows
python3 app.py                      # if you are on mac or linux
```

The backend server runs on the [http://localhost:9998](http://localhost:9998) port. You can open this link in the browser to see the swagger doc of the backend API.

