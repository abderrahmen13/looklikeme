import os
from flask import Flask, flash, render_template, request, redirect, url_for
from face_rec import classify_face
from werkzeug.utils import secure_filename
import urllib.request

UPLOAD_FOLDER = 'C:/Users/info-03/Desktop/abderrahmen/lookLikeMe/Flask web'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<id>', methods=['GET'])         # for mobile
def upload(id):
    # save file from url to current folder
    urllib.request.urlretrieve("http://looklikeme.cv-abderrahmen.esy.es/faces/"+id, id) # 'im' must end with .jpg...
    data = classify_face(id)
    # move file to faces folder
    os.rename(app.config['UPLOAD_FOLDER']+'/'+id, app.config['UPLOAD_FOLDER']+'/faces/'+id)
    return str(data).strip('[]')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])             # for web
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save file from <input> to current folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = classify_face(filename)
            # save file to database and get the id ...
            # rename file to Id ...
            # move file to faces folder
            os.rename(app.config['UPLOAD_FOLDER']+'/'+filename, app.config['UPLOAD_FOLDER']+'/faces/'+filename)
            return str(data).strip('[]')


if __name__ == '__main__':
    app.run(debug=True)