import pdfplumber
import xlsxwriter
import sys
import os
from seite import Seite

class Haushalt:
	def __init__(self, pdf_filename, name, jahr):
		self.pdf_filename = pdf_filename
		self.name = name
		self.jahr = jahr
		self.pages = []
		self.rows = []
		self.cache_dir = "page_cache_" + str(jahr)
	
	def extract_text_from_pdf(self):
		if not os.path.exists(self.cache_dir):
			print("Extrahiere Text aus dem PDF-Dokument...")
			os.mkdir(self.cache_dir)

			with pdfplumber.open(pdf_filename) as pdf:
				pages_count = len(pdf.pages);
				for page_number in range(pages_count):
					page_text = str(pdf.pages[page_number].extract_text())
					f = open(os.path.join(self.cache_dir, "{0:0=3d}".format(page_number + 1) + ".txt"), "w")
					f.write(page_text)
					f.close()
		else:
			print("Das Verzeichnis '" + self.cache_dir + "' existiert bereits! Löschen, um Extraktion erneut durchzuführen!")
	
	def read_pages_from_text_files(self):
		print("Verarbeite Textdateien aus '" + self.cache_dir + "'...")

		files = [f for f in os.listdir(self.cache_dir) if os.path.isfile(os.path.join(self.cache_dir, f))]
		for file_name in sorted(files):
			page_number = int(file_name[0:3])
			with open(os.path.join(self.cache_dir, file_name), "r") as myfile:
				page_lines = myfile.readlines()
				self.add_page(page_number, page_lines)
	
	def write_data_to_excel(self):
		print("Schreibe Excel-Sheet mit Daten...")

		workbook = xlsxwriter.Workbook("Data.xlsx")
		worksheet = workbook.add_worksheet()

		for i in range(0, len(self.rows)):
			row = self.rows[i]
			for j in range(0, len(row)):
				column = row[j]
				worksheet.write(i, j, column)

		workbook.close()
	
	def write_product_list_to_excel(self):
		print("Schreibe Excel-Sheet für Produkte...")
		workbook = xlsxwriter.Workbook("Produkte.xlsx")
		worksheet = workbook.add_worksheet()
		produkte = self.get_produkte()

		for i in range(0, len(produkte)):
			row = produkte[i]
			for j in range(0, len(row)):
				column = row[j]
				worksheet.write(i, j, column)

		workbook.close()

	def add_page(self, page_number, page_lines):
		if self.is_page_relevant(page_lines, page_number):
			p = Seite(self.name, self.jahr, page_number, page_lines)
			self.pages.append(p)

			rows = p.extract_rows()
			if self.check_result(rows):
				self.rows.extend(rows)
			else:
				print("Something not ok with " + p.meta)
	
	def check_result(self, rows):
		return len(rows) - len([x for x in rows if x[6] == 'TF']) - len([x for x in rows if x[6] == 'TE']) == 0

	def is_page_relevant(self, page_lines, page_number):
		if len(page_lines) > 3:

			if not page_lines[3].startswith("Produkt"):
				page_lines[2] = page_lines[2] + page_lines[3]
				del page_lines[3]

			if (page_lines[0].startswith("Doppischer Produktplan") and 
				page_lines[1].startswith("Produktbereich") and 
				page_lines[3].startswith("Produkt ") and
				any("Steuern und ähnliche" in s for s in page_lines)):
					return True
		
		return False
	
	def get_produkte(self):
		produkte = []
		
		for i in range(0, len(self.pages)):
			page = self.pages[i]
			if page.meta["typ"] == "TF":
				produkte.append([page.meta["obergruppe"], page.meta["mittelgruppe"], page.meta["untergruppe"], page.meta["name"], page.meta["rechtsbindung"]])
		
		return produkte