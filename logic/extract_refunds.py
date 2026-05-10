from pypdf import PdfReader
import os
import sys

# Set stdout encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

files = [
    r"C:\Root_entity\audits\refund from OpenAI OpCo.pdf",
    r"C:\Root_entity\audits\Refund-3290-6097.pdf",
    r"C:\Root_entity\audits\Refund-3810-0041.pdf"
]

for file_path in files:
    print(f"--- {os.path.basename(file_path)} ---")
    if not os.path.exists(file_path):
        print("File not found.")
        continue
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            print(page.extract_text())
    except Exception as e:
        print(f"Error: {e}")
    print("\n")
