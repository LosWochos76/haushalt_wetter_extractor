# Extractor-Script für PDF-Dateien des Haushalts der Stadt Wetter (Ruhr)

Der Haushaltsplan einer Gemeinde dient bekanntlich zur Feststellung des
gesamten Finanzbedarfs für die Erfüllung aller Aufgaben im kommenden Haushaltsjahrs, 
siehe: https://de.wikipedia.org/wiki/Haushaltsplan.

Der Haushaltsplan ist damit insb. für die kommunalpolitische Arbeit ein extrem
wichtiges Dokument. Die wichtigsten Debatten im Rat und den angeschlossenen Gremien
drehen sich um die Priorisierung von Aufgaben, wozu selbstverständlich die 
Fraktionen meist sehr unterschiedliche Ideen haben.

In der Stadt Wetter (Ruhr) wird der Entwurf des Haushalts durch den Kämmerer 
jährlich in Form einer PDF-Datei auf den Web-Seiten der Stadtverwaltung abgelegt, 
siehe: https://www.stadt-wetter.de/servicein-wetter/haushalt/.

Dieses Dokument zerfällt in Produkte, die wiederum hierarchisch in Produktbereiche und 
Produktgruppen gegliedert sind, z.B. 03.01.02 Gemeinschaftsgrundschule Alt-Wetter.
Zu jedem Produkt findet sich ein Teilergebnisplan (Erträge und Aufwendungen) und ein 
Teilfinanzplan (Einzahlungen und Auszahlungen), der die Angaben für festgelegte Positionen
enthält, z.B. Personalauszahlungen für das kommende Haushaltsjahr.

Es ist mitunter mühsam, den Haushaltsplan rein auf Basis dieser PDF-Dokumente zu analysieren und zu bewerten.
Leichter fällt es, wenn die Daten in Form eines Excel-Sheets vorliegen und ggf. auch
gegenüber anderen z.B. vorherigen Haushaltsplänen verglichen werden können.

## Script

Das Python-Script in diesem Repository dient dazu, die Daten aus dem PDF-Dokument eines Haushaltsplans 
zu extrahieren und in einem Excel-Sheet zu speichern. Um die Daten besser filtern 
und aggregieren zu können, wird eine einzelne Angabe aus dem Haushalt in Excel in genau
einer Zeile abgelegt, z.B. die Personalauszahlungen (Position 10) des Finanzplans für Produkt 
03.01.02 für das kommende Haushaltsjahr.

Es werden zudem lediglich die untersten Produktebenen exportiert. Die Sammler der Produkte 
werden nicht extrahiert, da die Summen ja leicht aus den untersten Produktebenen berechnet werden können.

Das Excel-Sheet, welches durch den Export entsteht, besitzt die folgenden Spalten:
- Dokument: Der Name des Quelldokuments, z.B. 'Haushaltsplan 2020'
- Seite: Die Seite, auf welcher der spezifische Wert zu finden ist.
- Obergruppe: Der Produktbereich
- Mittelgruppe: Die Produktgruppe
- Untergruppe: Die Produktnummer
- Rechtsbindung: F=Freiwillig, PO=Pflicht ohne Gestaltungsspielraum, PM=Pflicht mit Gestaltungsspielraum
- Typ: TE=Teilergebnisplan, TF=Teilfinanzplan
- Ansatz: Das Jahr, für den der Wert angesetzt ist.
- Wert: Der eigentliche Wert in Euro

## Nutzung

Um das Script zu nutzen, muss das PDF-Dokument des Haushalts im lokalen Ordner abgelegt werden.
Zudem müssen die beiden Python-Pakete "pdfplumber" und "xlsxwriter" installiert sein.
Danach kann der Haushalt wie folgt extrahiert werden:

```python
from budget import Budget

budget = Budget('Haushaltsplan_2021.pdf', 2021)
budget.extract_text_from_pdf()
budget.read_pages_from_text_files()
budget.write_data_to_excel()
budget.write_product_list_to_excel()
```

Die Kernarbeit wird dabei durch die Klasse Budget in mehreren Schritten durchgeführt.
Als Ergebnis liegen dann zwei Excel-Sheets vor: 
- Data_2021.xlsx: Die reinen Nutzdaten aus dem PDF-Dokument
- Produkte_2021.xlsx: Die Liste der Produkte aus dem PDF-Dokument

## Hinweise

Es bietet sich natürlich an, die Extraktion für mehrere Haushalte durchzuführen und
das Ergebnis in einem gemeinsamen Excel-Sheet abzulegen. Mit Hilfe von
Pivot-Tabellen usw. lässt sich dann eine ziemlich exakte Analyse durchführen.

Achtung: Die Nutzung erfolgt auf eigene Gefahr. Getestet wurde das Script für den
Haushaltsentwurf 2021 und den Haushalt 2020.