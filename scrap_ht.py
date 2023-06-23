from bs4 import BeautifulSoup
import re

with open('index_two.html', 'r') as f:
	doc = BeautifulSoup(f, 'html.parser')

tags = doc.find_all(string=re.compile('\$.*'), limit=13)
for i in tags:
	i.strip()
	print(i)
print(tags)

r'C:\Users\bucks\Downloads\chromedriver_win32\chromedriver.exe'