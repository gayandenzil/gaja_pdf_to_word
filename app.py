from flask import Flask, request, send_file, render_template
from pdf2docx import Converter
import os
import uuid

app = Flask(__name__, template_folder='templates')

# Project temp folder
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMP_FOLDER = os.path.join(PROJECT_ROOT, "temp_uploads")
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def convert_pdf_to_word():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return "No file uploaded", 400
            
        file = request.files["pdf_file"]
        if file.filename == "":
            return "No file selected", 400
        
        # Preserve original filename (without .pdf)
        original_name = os.path.splitext(file.filename)[0]
        output_filename = f"{original_name}.docx"
        
        pdf_path = os.path.join(TEMP_FOLDER, f"temp_{uuid.uuid4().hex}.pdf")
        word_path = os.path.join(TEMP_FOLDER, output_filename)
        
        try:
            # Save uploaded file
            file.save(pdf_path)
            
            # Convert PDF to Word
            cv = Converter(pdf_path)
            cv.convert(word_path)
            cv.close()
            
            # Render template with download link
            return render_template('index.html',
                show_output=True,
                output_filename=output_filename,
                download_url=f"/download/{output_filename}"
            )
            
        except Exception as e:
            if os.path.exists(pdf_path): os.remove(pdf_path)
            if os.path.exists(word_path): os.remove(word_path)
            return f"Error: {str(e)}", 500

    return render_template('index.html', show_output=False)

@app.route("/download/<filename>")
def download_file(filename):
    word_path = os.path.join(TEMP_FOLDER, filename)
    if os.path.exists(word_path):
        response = send_file(
            word_path,
            as_attachment=True,
            download_name=filename
        )
        
        # Schedule cleanup after download
        @response.call_on_close
        def cleanup():
            try:
                # Remove both PDF and DOCX versions
                temp_pdf = os.path.join(TEMP_FOLDER, f"temp_{filename.replace('.docx', '')}.pdf")
                if os.path.exists(temp_pdf): os.remove(temp_pdf)
                if os.path.exists(word_path): os.remove(word_path)
            except:
                pass
                
        return response
    return "File not found", 404


@app.route("/tempinfo")
def temp_info():
    return {
        "project_root": PROJECT_ROOT,
        "temp_folder": TEMP_FOLDER,
        "exists": os.path.exists(TEMP_FOLDER)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)