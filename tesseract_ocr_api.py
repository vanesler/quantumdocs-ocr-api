
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import os
import io

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    try:
        if filename.lower().endswith(".pdf"):
            # OCR for PDFs
            text_output = ""
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for page in doc:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                text_output += pytesseract.image_to_string(img) + "\n"
            return jsonify({'text': text_output})
        else:
            # OCR for image files
            img = Image.open(file.stream)
            text = pytesseract.image_to_string(img)
            return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'QuantumDocs OCR API is running'

if __name__ == '__main__':
    app.run(debug=True)
