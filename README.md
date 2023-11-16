# Student Industry Capstone Project Management System

## Download the code

The project repository is on the [github link here](https://github.com/unsw-cse-comp3900-9900-23T3/capstone-project-3900h11aikun). You can either `git clone` the code, or download the code in a zip file.

```
git clone git@github.com:unsw-cse-comp3900-9900-23T3/capstone-project-3900h11aikun.git
```

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

