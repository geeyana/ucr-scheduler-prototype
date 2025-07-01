"""
Program:        json-to-sql.py
Description:    Converts JSON file of courses to SQL table.
Last updated:   6/26/2025
"""

import json
import mysql.connector

# Read courses from JSON
with open("courses.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

# Connect to MySQL
conn = mysql.connector.connect(
    host = "XXX.X.X.X",
    user = "root",
    password = "XXXX",
    database = "courses"
)
cursor = conn.cursor()

# Delete all existing data
cursor.execute("DROP TABLE IF EXISTS courses_table")

# Create table if not exists (Note: This does not get all categories)
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses_table (
    id INT,
    term VARCHAR(10),
    courseReferenceNumber VARCHAR(10),
    courseTitle TEXT,
    subject VARCHAR(10),
    enrollment INT,
    seatsAvailable INT
)
"""
)

# Insert data
for course in courses:
    cursor.execute(
        """
        INSERT INTO courses_table (id, term, courseReferenceNumber, courseTitle, subject, enrollment, seatsAvailable)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, 
        (
        course["id"],
        course["term"],
        course["courseReferenceNumber"],
        course["courseTitle"],
        course["subject"],
        course["enrollment"],
        course["seatsAvailable"]
        )
    )

conn.commit()
conn.close()

print("\nJSON converted to MySQL.\n")