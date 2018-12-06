from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib.request

my_url = 'https://smsreceivefree.com/country/canada'
my_url2 = 'https://smsreceivefree.com/country/usa'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
cookie = '__cfduid=dedf3efcf3a477836d14c64e700daf0351534911645; SMSRF_SESSION=ff47967bc909ae17b409aca094dd35245f419c0f-___TS=2399433596383&id=ce36b88ecb14eee3113624cc8fc68e06e08d8d6c; _ga=GA1.2.115159071.1534911647; _gid=GA1.2.1563421996.1535369551'
headers={'User-Agent':user_agent,'cookie': cookie} 

request=urllib.request.Request(my_url,None,headers)
request2=urllib.request.Request(my_url2,None,headers)

uClient = uReq(request)
page_html = uClient.read()
uClient.close()

uClient = uReq(request2)
page_html2 = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
page_soup2 = soup(page_html2, "html.parser")

containers = page_soup.findAll("div", {"class":"row numview"})
containers2 = page_soup2.findAll("div", {"class":"row numview"})

filename = "numbers.csv"
f = open(filename, 'w')

headers = "№; Номер; Ссылка;\n"
f.write(headers)
x = 1
f.write('USA' + '\n')

for container in containers2:

	number = container.a.text
	numbers = number.split('(')
	number = numbers[0]
	link = container.a["href"]

	f.write( str(x) + ";" + number + ";" + link + "\n")
	x += 1

f.write('Canada' + '\n')
x = 1
for container in containers:

	number = container.a.text
	numbers = number.split('(')
	number = numbers[0]
	link = container.a["href"]

	f.write( str(x) + ";" + number + ";" + link + "\n")
	x += 1

f.close()
print("numbers.csv with numbers created")