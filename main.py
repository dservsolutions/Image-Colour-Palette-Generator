import os
import colorgram
import webcolors
from PIL import Image
from flask import Flask, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename, redirect

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_uploaded = {}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filename = None
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            print(f"Saved to {path}")

    return render_template('index.html', filename=filename)

# After processing the image, tells to the user what are the top 10 most common colors.
# Color - color code - percentage
def get_image_colors(image_path, num_colors=10):
    pass
if __name__ == '__main__':
    app.run(debug=True)