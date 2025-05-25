from pdfminer.high_level import extract_text
import json 
from datetime import datetime
import logging 
import re

logging.getLogger("pdfminer").setLevel(logging.ERROR)

class PDFParser():

    def __init__(self):
        pass

    def extract_clean_text_from_pdf(self, pdf_path):
        text = self.extract_text_from_pdf(pdf_path)
        return self.preprocess_text(text)

    def extract_text_from_pdf(self, pdf_path):
        """
        Estrae il testo dal PDF utilizzando pdfminer (per PDF nativi).
        """
        try:
            text = extract_text(pdf_path)
            return text
        except Exception as e:
            print("Errore nell'estrazione:", e)
            return ""
        
    def preprocess_text(self, text):
        """
        Normalizza il testo: minuscolo, rimozione punteggiatura e spazi multipli.
        """
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'[^A-Za-z0-9 ]+', ' ', text)
        return text.strip()
    
    def normalize_text(self, text):
        text_norm = re.sub(r'[^A-Za-z0-9 ]+', ' ', text)
        return text_norm

    def preprocess_text_list(self, lista):
        lista_pulita = []
        for elemento in lista:
            # Rimuove spazi iniziali e finali
            elemento = elemento.strip()
            # Rimuove caratteri speciali inutili
            elemento = self.preprocess_text(elemento)
            lista_pulita.append(elemento)
        return lista_pulita

    def create_json(self, text, pdf_path:str):
        output_filename = f"vector_data/{pdf_path.split('/')[-1].replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d_%S')}.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(text, f, indent=2)