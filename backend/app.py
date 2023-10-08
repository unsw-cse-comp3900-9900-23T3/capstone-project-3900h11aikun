from config import app

# serve the image directly
@app.route('/db/raw_data/avatars/<path:filename>', methods=['GET'])
def get_avatar(filename):
    return app.send_static_file(filename)


if __name__ == '__main__':
    # run on the 9998 port
    app.run(debug=True, port=9998)

