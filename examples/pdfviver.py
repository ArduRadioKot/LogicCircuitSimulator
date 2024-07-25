import tkinter as tk
from tkinter import filedialog
import PyPDF2

class PDFViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.open_button = tk.Button(self)
        self.open_button["text"] = "Open PDF"
        self.open_button["command"] = self.open_pdf
        self.open_button.pack(side="top")

        self.pdf_text = tk.Text(self)
        self.pdf_text.pack()

    def open_pdf(self):
        filename = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF files", "*.pdf")])
        if filename:
            pdf_file = open(filename, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            for page in range(num_pages):
                page_obj = pdf_reader.pages[page]
                self.pdf_text.insert(tk.END, page_obj.extract_text())
            pdf_file.close()

root = tk.Tk()
app = PDFViewer(master=root)
app.mainloop()