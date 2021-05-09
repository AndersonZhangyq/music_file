from flask import Flask, request, render_template
from flask_cors import CORS
import os

app = Flask(
    __name__,
    static_url_path="",
    template_folder="./front_end/dist/spa",
    static_folder="./front_end/dist/spa/static/",
)

# This is necessary because QUploader uses an AJAX request
# to send the file
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})


@app.route("/apis/upload", methods=["POST"])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        f.save("./uploads/%s" % fname)

    return "Okay!"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    if not os.path.exists("./uploads"):
        os.mkdir("./uploads")
    app.run(debug=True)
