from config import app

if __name__ == '__main__':
    print('Starting the backend, keep it running on this terminal...')

    # run on the 9998 port
    app.run(debug=True, port=9998)

