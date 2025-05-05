import os
import colorgram
import webcolors
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

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
    colors_data = []
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            colors = get_image_colors(path)
            for color in colors:
                colors_data.append(color)
            return render_template('index.html', filename=filename, top_rgb=colors_data)
    return render_template('index.html', filename=filename)

# After processing the image, tells to the user what are the top 10 most common colors.
# Color - color code - percentage
def get_image_colors(image_path, num_colors=10):
    try:
        colors = colorgram.extract(image_path, num_colors)
        named_colors = []
        for color in colors:
            rgb = (color.rgb.r, color.rgb.b, color.rgb.g)
            try:
                # Try to get the exact HTML color name
                name = webcolors.rgb_to_name(rgb)
            except ValueError:
                # If no exact match, provide the hex code as a fallback
                name = webcolors.rgb_to_hex(rgb)
            named_colors.append({'rgb': rgb, 'name': name})
        return named_colors
    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
        return  None
    except Exception as e:
        print(f" Error processing image: {e}")
        return None

    pass
if __name__ == '__main__':
    app.run(debug=True)