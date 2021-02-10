from haushalt import Haushalt

pdf_filename = 'Haushaltsplan_2020.pdf'
name = "Haushaltsplan 2020"
jahr = 2020

haushalt = Haushalt(pdf_filename, name, jahr)
haushalt.extract_text_from_pdf()
haushalt.read_pages_from_text_files()
haushalt.write_data_to_excel()
haushalt.write_product_list_to_excel()