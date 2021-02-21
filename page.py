import sys
import re
from decimal import *

class Page:
	def __init__(self, source_year, page_number, page_lines):
		self.meta = {}
		self.meta["source_year"] = source_year
		self.meta["page_number"] = page_number
		self.page_lines = page_lines
		self.page_lines.pop()
	
	def _extract_key_infos(self):
		name_string = self.page_lines[3]

		number = name_string[8:16].split(".")
		self.meta["number"] = name_string[8:16]
		self.meta["obergruppe"] = int(number[0])
		self.meta["mittelgruppe"] = int(number[1])
		self.meta["untergruppe"] = int(number[2])

		pos = name_string.find("bindung")-6
		self.meta["name"] = name_string[17:pos-1]
		rechtsbindung = name_string[pos+14:-1]
		
		if (rechtsbindung.find("mit") != -1):
			self.meta["rechtsbindung"] = "PM"
		
		if (rechtsbindung.find("ohne") != -1):
			self.meta["rechtsbindung"] = "PO"
		
		if (rechtsbindung.find("freiwillige") != -1):
			self.meta["rechtsbindung"] = "F"

		if (any("Teilfinanzplan" in s for s in self.page_lines)):
			self.meta["typ"] = "TF"
		else:
			self.meta["typ"] = "TE"

	def is_page_relevant(self):
		if len(self.page_lines) > 3:

			if not self.page_lines[3].startswith("Produkt"):
				self.page_lines[2] = self.page_lines[2] + self.page_lines[3]
				del self.page_lines[3]

			if (self.page_lines[0].startswith("Doppischer Produktplan") and 
				self.page_lines[1].startswith("Produktbereich") and 
				self.page_lines[3].startswith("Produkt ") and
				any("Steuern und ähnliche" in s for s in self.page_lines)):
					return True

		return False

	def extract_data(self):
		self._extract_key_infos()
		rows = []

		for i in range(5, len(self.page_lines)):
			line = self.page_lines[i].strip()
			if not line:
				continue

			columns = self._extract_values_from_row(line)
			if columns == None:
				continue

			data = self._transform(columns)
			rows.extend(data)

		return rows

	def _extract_values_from_row(self, line):
		columns = []
		str = ""
		last_str = ""

		for i in range(len(line)-1, 0, -1):
			if line[i] != ' ' or len(columns) == 6:
				str = line[i] + str
				last_str = line[i]
			else:
				if str:
					columns.insert(0, str)
					str = ""

		columns.insert(0, line[0] + str)

		if len(columns) != 7:
			return None

		match = re.search('^(\d+)[\s+\+\-\=]{1}', columns[0])
		if (match):
			columns[0] = int(match.group(1))
		
		for i in range(1,len(columns)):
			columns[i] = Decimal(columns[i].replace(".", "").replace(",", "."))

		return columns

	def _transform(self, columns):
		rows = []

		for i in range(1, len(columns)):
			line = {}
			line['Quelle'] = self.meta["source_year"]
			line['Seite'] = self.meta["page_number"]
			line['Produktbereich'] = self.meta["obergruppe"]
			line['Produktgruppe'] = self.meta["mittelgruppe"]
			line['Produkt'] = self.meta["untergruppe"]
			line['Rechtsbindung'] = self.meta["rechtsbindung"]
			line['Typ'] = self.meta["typ"]
			line['Position'] = int(columns[0])
			line['Ansatz'] = self.meta["source_year"] - 3 + i
			line['Wert'] = float(columns[i])
			rows.append(line)
		
		return rows

	def __str__(self):
			return str(self.meta)