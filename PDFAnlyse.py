import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize

# Ensure the punkt data is downloaded
nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text, doc.page_count

def analyze_text(text):
    sentences = sent_tokenize(text)
    num_sentences = len(sentences)
    total_length = sum(len(sentence.split()) for sentence in sentences)
    average_sentence_length = total_length / num_sentences if num_sentences > 0 else 0
    return num_sentences, average_sentence_length

if __name__ == "__main__":
    pdf_path = r"C:\Users\isabe\OneDrive\Desktop\Fachpraktikum\TestAbschlussarbeiten\bachelorarbeit_gundula_swidersky.pdf"  # Replace with your PDF file path
    text, num_pages = extract_text_from_pdf(pdf_path)
    num_sentences, avg_sentence_length = analyze_text(text)
    print(f"Number of pages: {num_pages}")
    print(f"Number of sentences: {num_sentences}")
    print(f"Average sentence length: {avg_sentence_length:.2f} words")
    

