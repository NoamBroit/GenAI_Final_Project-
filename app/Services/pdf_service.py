import PyPDF2

class PDFService:
    @staticmethod
    def extract_text(file_path):
        text = ""
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text