import urllib.request
import re
import webbrowser

def getCourseNumbers(addedURL):
    url = addedURL
    html = urllib.request.urlopen(url).read().decode('utf-8')
    courses = re.findall(r'https://drive.google.com/file/(.*?)"',html)
    return set(courses)

def open_urls(course_numbers):
	base_url_each_syllabi = url = 'https://drive.google.com/file/';
	for course_num in course_numbers:
		url = base_url_each_syllabi + str(course_num)
		webbrowser.open(url, new=0, autoraise=True)

all_syllabi_url = 'http://www.austincc.edu/offices/academic-outcomes-assessment/master-syllabi/master-syllabi-repository'
course_numbers = getCourseNumbers(all_syllabi_url)
print(len(course_numbers))
open_urls(list(course_numbers)[0:10])