from config import app
from flask import send_from_directory


# serve the image directly
@app.route('/db/raw_data/avatars/<path:filename>', methods=['GET'])
def get_avatar(filename):
    return app.send_static_file(filename)


# serve any uploads directly
@app.route('/uploads/<path:filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # run on the 9998 port
    app.run(debug=True, port=9998)

