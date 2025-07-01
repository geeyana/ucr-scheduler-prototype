"""
Program:        json-to-csv.py
Description:    Converts JSON file of courses to CSV table.
Last updated:   6/26/2025
"""

import pandas as pd
import json

with open('courses.json', encoding='utf-8') as f:
    df = pd.read_json(f)

df.to_csv('courses.csv', encoding='utf-8', index=False)

print("\nJSON converted to CSV.\n")