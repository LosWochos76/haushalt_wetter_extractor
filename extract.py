from budget import Budget

budget = Budget('Haushaltsplan_2021.pdf', 2021)
budget.extract_text_from_pdf()
budget.read_pages_from_text_files()
budget.write_data_to_excel()
budget.write_product_list_to_excel()