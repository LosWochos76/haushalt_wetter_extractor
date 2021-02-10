import sys
import re
import pandas as pd

class Product:
	def __init__(self, line1, line2, f):
		self.line1 = line1
		self.line2 = line2
		self.f = f

		fl = line1.splitlines()
		name_string = fl[3]

		self.number = name_string[8:16]
		pos = name_string.find("Rechtsbindung")
		self.name = name_string[17:pos-1]
		self.rechtsbindung = name_string[pos+14:]

		self.f.write(self.number + "\n")
		self.f.write(self.name + "\n")
		self.f.write(self.rechtsbindung + "\n")

		self.create_table(line1)
		self.create_table(line2)

	def create_table(self, line):
		lines = line.splitlines()
		lines.pop()

		self.f.write(lines[4] + "\n")

		columns = []
		if (lines[4].find("Teilergebnisplan")):
			columns = ["Teilergebnisplan (ab 2020)", "Ergebnis 2019", "Ansatz 2020", "Ansatz 2021", "Planung 2022", "Planung 2023", "Planung 2024"]
		else:
			columns = ["Teilfinanzplan - Zahlungsübersicht", "Ergebnis 2019", "Ansatz 2020 ", "Ansatz 2021", "Planung 2022", "Planung 2023", "Planung 2024"]

		df = pd.DataFrame(columns = columns)

		for i in range(5, len(lines)):
			lines[i] = lines[i].strip()
			if lines[i]:
				self.f.write(lines[i] + "\n")
				self.extract_columns(lines[i])

	def extract_columns(self, line):
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
			print(columns)

	def write_to_workbook(self, workbook):
		 worksheet = workbook.add_worksheet(self.number)
		 worksheet.write_string(0, 0, self.number)
		 worksheet.write_string(1, 0, self.name)
		 worksheet.write_string(2, 0, self.rechtsbindung)

	def __str__(self):
			return self.number + ": " + self.name