import pandas as pd
import re
from fuzzywuzzy import fuzz

class DetectionAgent:
    def __init__(self, df):
        self.df = df
        self.logs = []

    def detect_missing(self):
        missing = self.df[self.df.isnull().any(axis=1)]
        self.logs.append(f"Found {len(missing)} rows with missing values")
        return missing

    def detect_malformed_emails(self):
        pattern = r'^\S+@\S+\.\S+$'
        invalid = self.df[~self.df['email'].astype(str).str.match(pattern)]
        self.logs.append(f"Found {len(invalid)} malformed email addresses")
        return invalid

    def detect_duplicates(self):
        duplicates = self.df[self.df.duplicated()]
        self.logs.append(f"Found {len(duplicates)} duplicate rows")
        return duplicates

    def run(self):
        self.detect_missing()
        self.detect_malformed_emails()
        self.detect_duplicates()
        return self.logs
