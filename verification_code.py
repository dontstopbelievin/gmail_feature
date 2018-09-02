from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib.request
import time

class Phone_Messages(object):

	def __init__(self, phone_link):
		self.my_url = f'https://smsreceivefree.com{phone_link}'
		self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		self.cookie = '__cfduid=dedf3efcf3a477836d14c64e700daf0351534911645; SMSRF_SESSION=ff47967bc909ae17b409aca094dd35245f419c0f-___TS=2399433596383&id=ce36b88ecb14eee3113624cc8fc68e06e08d8d6c; _ga=GA1.2.115159071.1534911647; _gid=GA1.2.1563421996.1535369551'
		self.headers = {'User-Agent': self.user_agent,'cookie': self.cookie}
		self.request = urllib.request.Request( self.my_url, None, self.headers)
		self.response = ''

	def get_code(self):
		uClient = uReq(self.request)
		page_html = uClient.read()
		uClient.close()
		page_soup = soup(page_html, "html.parser")
		containers = page_soup.findAll("tr")
		for container in containers:
			tds = container.findAll("td")
			if len(tds) == 3:
				msg = tds[2].text.strip()
				strs = msg.split("-")
				if len(strs) == 2 and strs[0].strip() =='G':
					strs2 = strs[1].split("–")
					if len(strs2) == 2 and strs2[1].strip() == 'Ваш проверочный код.':
						self.response = strs2[0]
						return True
		return False