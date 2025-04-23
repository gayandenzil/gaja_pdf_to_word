# simple PDF Converter/

from pdf2docx import Converter
from docx import Document

def convert_pdf_to_word(pdf_file, word_file):
    try:
        # Create a PDF converter object
        fileToConvert = Converter(pdf_file)
        
        # Convert PDF to Word
        fileToConvert.convert(word_file, start=0, end=None)
        
        # Close the converter
        fileToConvert.close()

        print(f"✅ Successfully converted '{pdf_file}' to '{word_file}'")
    except Exception as e:
        print(f"❌ Error: {e}")


pdf_path = input("Enter the full path to the PDF file: ").strip('"')
word_path = input("Enter the full path for the output Word file (e.g., output.docx): ").strip('"')
convert_pdf_to_word(pdf_path, word_path)

