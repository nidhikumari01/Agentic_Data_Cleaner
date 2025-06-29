# 🧹 Agentic Data Cleaning & Enrichment Pipeline

This project implements a modular **agent-based data cleaning system** that processes messy customer record CSVs using a sequence of intelligent agents. Each agent handles a distinct task—**detection**, **correction**, and **enrichment**—creating a lightweight and self-fixing pipeline.

---

##  Features

- **Detection Agent**  
  Identifies:
  - Missing or malformed fields (e.g., invalid emails)
  - Duplicate records
  - Incorrect or misspelled values (e.g., country names)

- **Correction Agent**  
  Applies fixes:
  - Standardizes values (e.g., name formatting)
  - Removes duplicates
  - Uses fuzzy matching to correct country names

- **Enrichment Agent**  
  Adds value:
  - Fills missing fields (via LLMs)
  - Derives new attributes (e.g., inferred location info)

- **UI Agent** *  
  Simple Streamlit or CLI interface to:
  - Upload raw CSV
  - View & download cleaned output

---

## Project Demo Live


## Install Dependencies

pip install -r requirements.txt

## Run the Streamlit UI

streamlit run app.py
Upload sample.csv file 

