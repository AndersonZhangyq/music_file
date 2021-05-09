from flask import Flask, request, render_template, jsonify
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
cors.init_app(app, resource={r"/apis/*": {"origins": "*"}})


@app.route("/apis/upload", methods=["POST"])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        f.save("./uploads/%s" % fname)

    return "OKAY!"

@app.route("/apis/submit", methods=["POST"])
def submit():
    return jsonify(
        [
            {"src": "https://cdn.quasar.dev/img/mountains.jpg", "alt": "mountain"},
            {
                "src": "https://d33wubrfki0l68.cloudfront.net/28e392e11daadef180e12e890014c81dec12bd0c/3738d/image-4.a4d08f7d.jpg",
                "alt": "cat",
            },
        ]
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    if not os.path.exists("./uploads"):
        os.mkdir("./uploads")
    app.run(debug=True)
