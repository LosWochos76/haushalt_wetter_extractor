import pdfplumber
import xlsxwriter
import sys
import os
import pandas as pd
from page import Page

class Budget:
	def __init__(self, pdf_filename, year):
		self.pdf_filename = pdf_filename
		self.source_year = year
		self.cache_dir = "page_cache_" + str(year)
		self.pages = []
		self.dataframe = pd.DataFrame(columns=['Quelle','Seite','Produktbereich','Produktgruppe','Produkt','Rechtsbindung','Typ','Position','Ansatz','Wert'])
	
	def extract_text_from_pdf(self):
		if not os.path.exists(self.cache_dir):
			print("Extrahiere Text aus dem PDF-Dokument...")
			os.mkdir(self.cache_dir)

			with pdfplumber.open(self.pdf_filename) as pdf:
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
				self._add_page(page_number, page_lines)
	
	def write_data_to_excel(self):
		print("Schreibe Excel-Sheet mit Daten...")

		filename = "Data_" + str(self.source_year) + ".xlsx"
		writer = pd.ExcelWriter(filename, engine='xlsxwriter')
		self.dataframe.to_excel(writer, index=False)
		writer.save()
	
	def write_product_list_to_excel(self):
		print("Schreibe Excel-Sheet für Produkte...")
		workbook = xlsxwriter.Workbook("Produkte_" + str(self.source_year) + ".xlsx")
		worksheet = workbook.add_worksheet()
		produkte = self.get_produkte()

		for i in range(0, len(produkte)):
			row = produkte[i]
			for j in range(0, len(row)):
				column = row[j]
				worksheet.write(i, j, column)

		workbook.close()

	def _add_page(self, page_number, page_lines):
		p = Page(self.source_year, page_number, page_lines)

		if p.is_page_relevant():
			self.pages.append(p)
			rows = p.extract_data()
			self.dataframe = self.dataframe.append(rows, ignore_index=True)
		
	def get_produkte(self):
		produkte = []
		
		for i in range(0, len(self.pages)):
			page = self.pages[i]
			if page.meta["typ"] == "TF":
				produkte.append([page.meta["obergruppe"], page.meta["mittelgruppe"], page.meta["untergruppe"], page.meta["name"], page.meta["rechtsbindung"]])
		
		return produkte