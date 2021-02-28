import unittest
import requests
from budget import Budget

class TestBudget(unittest.TestCase):
    def setUp(self):
        url = 'https://www.stadt-wetter.de/fileadmin/user_upload/Dokumente/Fachbereich_1/2021_-_Haushaltsplanentwurf.pdf'
        r = requests.get(url, allow_redirects=True)
        file = open('Haushaltsplan_2021.pdf', 'wb')
        file.write(r.content)
        file.close()

        self.budget = Budget('Haushaltsplan_2021.pdf', 2021)
        self.budget.extract_text_from_pdf()
        self.budget.read_pages_from_text_files()
    
    def test_line_count(self):
        df = self.budget.dataframe
        self.assertEqual(36828, len(df.index))
    
    def test_saldo_verwaltungstaetigkeit(self):
        df = self.budget.dataframe
        new_df = df[(df.Ansatz == 2021) & (df.Typ == "TF") & (df.Position == 17)]
        self.assertEqual(-7784322, new_df['Wert'].sum())
    
    def test_ordentliches_ergebnis(self):
        df = self.budget.dataframe
        new_df = df[(df.Ansatz == 2021) & (df.Typ == "TE") & (df.Position == 18)]
        self.assertEqual(-5305205, new_df['Wert'].sum())

if __name__ == '__main__':
    unittest.main()