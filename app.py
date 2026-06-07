from flask import Flask, render_template, request
import easyocr
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

reader = easyocr.Reader(['en'])

@app.route("/", methods=["GET", "POST"])
def home():

    extracted_text = ""

    if request.method == "POST":

        image = request.files["image"]

        if image:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                image.filename
            )

            image.save(filepath)

            result = reader.readtext(
                filepath,
                detail=0
            )

            extracted_text = " ".join(result)

    return render_template(
        "index.html",
        extracted_text=extracted_text
    )

if __name__ == "__main__":
    app.run(debug=True)