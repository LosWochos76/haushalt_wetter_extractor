import sys
import re
import pandas as pd
from decimal import *

class Seite:
	def __init__(self, dokument, jahr, page_number, page_lines):
		self.meta = {}
		self.meta["dokument"] = dokument
		self.meta["jahr"] = jahr
		self.meta["seite"] = page_number
		
		page_lines.pop()
		self.page_lines = page_lines
		self.extract_key_infos()
	
	def extract_key_infos(self):
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

	def extract_rows(self):
		rows = []

		for i in range(5, len(self.page_lines)):
			self.page_lines[i] = self.page_lines[i].strip()
			if self.page_lines[i]:
				self.extract_single_row(self.page_lines[i], rows)

		return rows

	def extract_single_row(self, line, rows):
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

		if len(columns) == 7:
			match = re.search('^(\d+)[\s+\+\-\=]{1}', columns[0])
			if (match):
				columns[0] = int(match.group(1))
			
			for i in range(1,len(columns)):
				columns[i] = Decimal(columns[i].replace(".", "").replace(",", "."))

			self.split_rows(columns, rows)

	def split_rows(self, columns, rows):
		for i in range(1,len(columns)):
			row = []
			row.append(self.meta["dokument"])
			row.append(self.meta["seite"])
			row.append(self.meta["obergruppe"])
			row.append(self.meta["mittelgruppe"])
			row.append(self.meta["untergruppe"])
			row.append(self.meta["rechtsbindung"])
			row.append(self.meta["typ"])
			row.append(columns[0])
			row.append(self.meta["jahr"] - 3 + i)
			row.append(columns[i])
			rows.append(row)

	def __str__(self):
			return str(self.meta)