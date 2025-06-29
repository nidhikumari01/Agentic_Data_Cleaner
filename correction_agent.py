import pandas as pd
from fuzzywuzzy import process

class CorrectionAgent:
    def __init__(self, df):
        self.df = df.copy()
        self.logs = []
        self.valid_countries = [
            "USA", "India", "UK", "Nepal", "France", "Canada"
        ]

    def remove_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        self.logs.append(f"Removed {before - after} duplicate rows.")

    def fix_missing_values(self):
        # Option: Drop rows with any missing values
        before = len(self.df)
        self.df = self.df.dropna()
        after = len(self.df)
        self.logs.append(f"Dropped {before - after} rows with missing values.")

    def clean_whitespace_and_case(self):
        for col in ['name', 'email', 'country']:
            self.df[col] = self.df[col].astype(str).str.strip()
        self.df['name'] = self.df['name'].str.title()
        self.df['country'] = self.df['country'].str.title()

    def correct_country_names(self):
        def fix_country(name):
            best_match, score = process.extractOne(name, self.valid_countries)
            return best_match if score > 80 else name

        self.df['country'] = self.df['country'].apply(fix_country)
        self.logs.append("Corrected country names using fuzzy matching.")

    def run(self):
        self.clean_whitespace_and_case()
        self.remove_duplicates()
        self.fix_missing_values()
        self.correct_country_names()
        return self.df, self.logs
