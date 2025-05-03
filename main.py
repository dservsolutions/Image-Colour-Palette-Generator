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
            top10 = get_image_properties(path)
            if top10:
                color_name = webcolors.rgb_to_name(top10)
                print(color_name)

    return render_template('index.html', filename=filename)

# After processing the image, tells to the user what are the top 10 most common colors.
# Color - color code - percentage
def get_image_properties(image_path, num_colors=10):
    try :
        img = Image.open(image_path)
        properties = {
            "format" : img.format,
            "size": img.size,
            "mode": img.mode
        }
        colors = colorgram.extract(image_path, num_colors)
        top_colors = []
        for color in colors:
            # color.rgb is a named tuple with r, g, b attributes
            rgb_tuple = (color.rgb.r, color.rgb.g, color.rgb.b)
            # top_colors.append(rgb_tuple)
            top_colors.append(rgb_tuple)
            return top_colors
        return properties
    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
        return None


if __name__ == '__main__':
    app.run(debug=True)