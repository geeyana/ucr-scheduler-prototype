"""
Program:        get-course-data.py
Description:    Scrapes course data from UCR's registration website for students.
Last updated:   6/26/2025
"""

import json
import requests
from requests import get
from requests import request
from requests import Session
from requests.cookies import RequestsCookieJar

"""
term = YYYYSS

+----+----------+
| SS | Semester |
+----+----------+
| 10 | Winter   |
+----+----------+
| 20 | Spring   |
+----+----------+
| 30 | Summer   |
+----+----------+
| 40 | Fall     |
+----+----------+
"""
# For classes in Spring 2025
term = 202520

# First thing is to get the JSESSIONID 
# (This is a Java token sent back and forth between 
# client and server to handle client’s session). 

def main():
    pass

def fetch_course_description(course, term, headers):
    response = requests.post(
        "https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/getCourseDescription", headers=headers, data={"term": term, "courseReferenceNumber": course["courseReferenceNumber"]})
    return response

JSESSIONID = get("https://registrationssb.ucr.edu").cookies["JSESSIONID"]

# Setting headers for request
headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

r = request("POST", "https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/term/search?mode=search", data={"term": term})

jar = RequestsCookieJar()
jar.update(r.cookies)

pageOffset = 0
pageMaxSize = 500

# Initial request to get totalCount of courses
url = f"https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?&txt_term={term}&pageOffset={pageOffset}&pageMaxSize={pageMaxSize}&sortColumn=subjectDescription&sortDirection=asc"
response = request("GET", url, headers=headers, cookies=jar)
totalCount = response.json()["totalCount"]

pageMaxSize = 500  # Max request size
courses = []
unique_crn = set()
pageOffset = 0

while True:
    print(len(courses))
    url = f"https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?&txt_term={term}&startDatepicker=&endDatepicker=&pageOffset={pageOffset}&pageMaxSize={pageMaxSize}&sortColumn=subjectDescription&sortDirection=asc"
    response = request("GET", url, headers=headers, cookies=jar)
    response.raise_for_status()
    new_courses = response.json()["data"]
       
    if not new_courses:
        print("No more courses available.\n")
        break
   
    courses.extend(new_courses)

    if len(new_courses) < pageMaxSize:
        print("Fetched all available data.\n")
        break

    pageOffset += pageMaxSize # Getting next 500 sections

    if len(courses) >= totalCount:
        break

uniqueCourses = {}
for course_key in uniqueCourses:
    course = uniqueCourses[course_key]
    response = fetch_course_description(course, term, headers)

# Put data on a separate JSON file
with open("courses.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, indent=4)

if __name__ == '__main__':
	main()

print("\nCourse data obtained from Banner. Written to JSON file.\n")