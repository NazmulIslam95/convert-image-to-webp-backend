from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io
import zipfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        scale = float(request.form.get("scale", 0.5))
        images = request.files.getlist("images")

        # Get folder name from first image
        zip_filename = "converted-to-webp.zip"
        if images and "/" in images[0].filename:
            folder_name = images[0].filename.split("/")[0]
            zip_filename = f"{folder_name}-converted-to-webp.zip"

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zipf:
            for image in images:
                try:
                    img = Image.open(image).convert("RGB")
                    w, h = img.size
                    new_size = (int(w * scale), int(h * scale))
                    img_resized = img.resize(new_size, Image.LANCZOS)

                    base_name = os.path.splitext(os.path.basename(image.filename))[0]
                    output_name = f"{base_name}_edited.webp"

                    img_io = io.BytesIO()
                    img_resized.save(img_io, format="WEBP", quality=80)
                    img_io.seek(0)
                    zipf.writestr(output_name, img_io.read())
                except Exception as e:
                    print("❌ Error:", e)

        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=zip_filename,
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
# This code is a Flask application that allows users to upload images, resize them, and convert them to WebP format.
# It packages the converted images into a zip file for download.
# The application uses the Pillow library for image processing and handles file uploads through Flask's request object.
# The main route handles both GET and POST requests, processing the images and returning a zip file with the converted images.
