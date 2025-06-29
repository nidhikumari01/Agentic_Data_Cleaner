import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

class EnrichmentAgent:
    def __init__(self, df):
        self.df = df.copy()
        self.logs = []
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-70b-8192"

    def call_llm(self, prompt, max_tokens=15):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": max_tokens,
            }
            response = requests.post(self.api_url, headers=headers, json=body)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return "Unknown"

    def fill_missing_names(self):
        filled = 0
        for idx, row in self.df.iterrows():
            if pd.isna(row['name']) or row['name'].strip() == "":
                email = row.get("email", "")
                prompt = f"Guess a realistic first name from the email: {email}"
                guess = self.call_llm(prompt)
                if guess != "Unknown":
                    self.df.at[idx, "name"] = guess
                    filled += 1
        self.logs.append(f"🧩 Filled {filled} missing names using Groq LLM.")

    def add_customer_segment(self):
        segments = []
        for _, row in self.df.iterrows():
            email = row.get("email", "")
            prompt = f"What customer type is likely for this email: {email}? Respond with one word: Student, Professional, Retired, or Unknown."
            segment = self.call_llm(prompt)
            segments.append(segment)
        self.df["segment"] = segments
        self.logs.append("📦 Added 'segment' column.")

    def add_gender(self):
        genders = []
        for _, row in self.df.iterrows():
            name = row.get("name", "")
            email = row.get("email", "")
            prompt = f"Guess the likely gender (Male or Female) for this person based on name '{name}' and email '{email}'. Reply only with Male or Female."
            gender = self.call_llm(prompt)
            if gender.lower() in ["male", "female"]:
                genders.append(gender.capitalize())
            else:
                genders.append("Unknown")
        self.df["gender"] = genders
        self.logs.append("🚻 Added 'gender' column using Groq.")

    def run(self):
        self.fill_missing_names()
        self.add_customer_segment()
        self.add_gender()
        return self.df, self.logs
