import os
from flask import Flask, render_template, request, flash, redirect
from flask_assets import Environment
from webassets import loaders

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = "123"

# asset pipeline
assets = Environment(app)
bundles = loaders.YAMLLoader('./static/js/js-assets.yml').load_bundles()
[assets.register(name, bundle) for name, bundle in bundles.items()]
bundles = loaders.YAMLLoader('./static/styles/css-assets.yml').load_bundles()
[assets.register(name, bundle) for name, bundle in bundles.items()]


@app.route("/")
def index():
    return render_template('index.html', file_name="")

@app.route("/login")
def login():
    return render_template("login.html", fl="")

@app.route("/process_login", methods=['POST'])
def process_login():
    print(request.values['email'])
    if "fern" in request.values['email']:
        return render_template("recipes.html", fl="welcome back fernando")
    else:
        return render_template("login.html", fl="invalid login")

@app.route("/upload")
def upload():
    return render_template('upload.html', file_name="")


@app.route('/process_upload', methods=['GET', 'POST'])
def process_upload():
    print("in upload")
    if request.method == 'POST':
        print("In post")
        # check if the post request has the file part
        print(request)
        if 'file' not in request.files:
            flash('No file part')
            return render_template('upload.html', file_name="")

        file = request.files['file']
        print("filename: ", file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        file.save(os.path.join('/app', file.filename))

        return render_template('upload.html', file_name="Thanks for submitting %s. It looks tasty. --fernando" % file.filename)


@app.route('/jbbd')
def jbbd():
    return render_template('jbbd.html')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5001)
