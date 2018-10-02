from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from bs4 import BeautifulSoup
import urllib.request
import time

# Crawl phones numbers from smsreceivefree to file numbers.csv
import os.path
if not os.path.isfile("numbers.csv"):
	import phones
# Class to grab verf code from smsreceivefree.com
import verification_code

class wait_for_any_text(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            return len(EC._find_element(driver, self.locator).text.strip())
        except StaleElementReferenceException:
            return False

class GmailSignup(object):

	def __init__(self, firstname, lastname, username, password, phone_number, phone_link, my_host, my_port):
		self.url = f"https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default&flowName=GlifWebSignIn&flowEntry=SignUp"
		#self.driver = webdriver.Firefox(firefox_profile=self.setProxy(my_host, my_port))
		self.driver = webdriver.Firefox()
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.password = password
		self.phone_number = phone_number
		self.phone_link = phone_link
		self.delay = 20
		self.ver_code = ''

	def setProxy(self, my_host, my_port):
		profile = webdriver.FirefoxProfile()
		profile.set_preference("network.proxy.type", 1)
		profile.set_preference("network.proxy.http", my_host)
		profile.set_preference("network.proxy.http_port", my_port)
		profile.set_preference("network.proxy.ssl", my_host)
		profile.set_preference("network.proxy.ssl_port", my_port)
		return profile

	def laod_url(self):
		self.driver.get(self.url)
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.element_to_be_clickable((By.ID, "username")))
			print("Sign up page is ready")
		except TimeoutException:
			print("Loading took too much time")
			self.quit()

	def sign_up(self):
		self.driver.find_element_by_name('firstName').send_keys(self.firstname)
		self.driver.find_element_by_name('lastName').send_keys(self.lastname)
		self.driver.find_element_by_name('Username').send_keys(self.username)
		self.driver.find_element_by_name('Passwd').send_keys(self.password)
		self.driver.find_element_by_name('ConfirmPasswd').send_keys(self.password)
		self.driver.find_element_by_id('accountDetailsNext').click()
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.presence_of_element_located((By.ID, "headingText")))
			print("Sign up page proccessed")
		except TimeoutException:
			print("Loading took too much time")
			self.quit()

	def fill_in_info(self):
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.element_to_be_clickable((By.ID, "phoneNumberId")))
			print("Fill in info page is ready")
		except TimeoutException:
			print("Loading took too much time")
			self.quit()
		self.driver.find_element_by_id('phoneNumberId').clear()
		self.driver.find_element_by_id('day').send_keys('21')
		Select(self.driver.find_element_by_id('month')).select_by_index(1)
		self.driver.find_element_by_id('year').send_keys('1984')
		Select(self.driver.find_element_by_id('gender')).select_by_index(1)
		self.driver.find_element_by_id('personalDetailsNext').click()

	def confirm_rules(self):
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.presence_of_element_located((By.CLASS_NAME, "eLUXld")))
			print("Confirm rules page is ready")
		except TimeoutException:
			print("Confirm rules page: Loading took too much time")
			self.quit()
		content = self.driver.find_element_by_class_name('eLUXld')
		self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', content)
		
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.element_to_be_clickable((By.ID, "termsofserviceNext")))
			print("Confirm button ready")
			self.driver.find_element_by_id('termsofserviceNext').click()
		except TimeoutException:
			print("Confirm button: Loading took too much time")
			self.quit()
		
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bu0")))
			print("Google welcome page loaded")
			if self.driver.find_element_by_class_name('bu0').text.strip() == 'Добро пожаловать!':
				print('Account signed up ' + self.username)
			else:
				print('Error while confirmation')
		except TimeoutException:
			print("Google welcome page: Loading took too much time")
			self.quit()

	def send_sms(self):
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.element_to_be_clickable((By.ID, "phoneNumberId")))
			print("Send sms page is ready")
		except TimeoutException:
			print("Loading took too much time")
			self.quit()
			return False
		self.driver.find_element_by_id('phoneNumberId').clear()
		self.driver.find_element_by_id('phoneNumberId').send_keys(self.phone_number)
		self.driver.find_element_by_id('gradsIdvPhoneNext').click()
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(wait_for_any_text((By.CLASS_NAME, "dEOOab")))
			if self.driver.find_element_by_class_name('dEOOab').text.strip() == 'Этот номер нельзя использовать для подтверждения ID.':
				print('Number not useable for verification')
			else:
				if self.driver.find_element_by_class_name('dEOOab').text.strip() == 'Этот телефонный номер был использован слишком много раз.':
					print('Number used to many times')
				else:
					print('Another error message')
			self.quit()
			return False
		except TimeoutException:
			print('Sms must have been sent.')
			return True

	def get_code(self):
		counter = 1
		obj = verification_code.Phone_Messages(self.phone_link)
		while not obj.get_code():
			if counter == 30:
				print("Too many tries to grab code")
				self.quit()
			time.sleep(1)
			obj.get_code()
			print("get_code(): Trying again")
			counter += 1
		self.ver_code = obj.response

	def submit_code(self):
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.element_to_be_clickable((By.ID, "code")))
			print("Page is ready")
		except TimeoutException:
			print("Loading took too much time")
			self.quit()
		self.driver.find_element_by_id('code').send_keys(self.ver_code)
		self.driver.find_element_by_id('gradsIdvVerifyNext').click()

	def quit(self):
		print('Used number: ' + self.phone_number)
		#self.driver.close()
		#exit()

# Main application Runner:
# Put numbers from csv file to arr_phones
filename = "numbers.csv"
f = open(filename, 'r')
lines = f.readlines()
arr_phones = []
arr_links = []
for line in lines:
	items = line.split(";")
	if 1 < len(items):
		if "+1" not in items[1]:
			continue
		arr_phones.append(items[1].strip())
		arr_links.append(items[2].strip())

# Array to keep track of phones that can register only 3 accounts
# This is not used yet
#phones_used_count = [0] * len(arr_phones)

# Sign up credentials
firstname = 'app'
lastname = 'app'
user_number = 4
password = '123123Aa'

#Free proxy credentials
MY_HOST = "158.58.133.41"
MY_PORT = 32231

#not done: pass phones with check

for i in range(len(arr_phones)):
	username = f"astanamailer{user_number}"
	gmail_page = GmailSignup(firstname, lastname, username, password, arr_phones[i], arr_links[i], MY_HOST, MY_PORT)
	gmail_page.laod_url()
	gmail_page.sign_up()

	if gmail_page.driver.find_element_by_id('headingText').text.strip() == 'Добро пожаловать в Google':
		print('Number accepted')
		gmail_page.fill_in_info()
		gmail_page.confirm_rules()
		user_number += 1
	else:
		print('Sending sms')
		if gmail_page.send_sms() == False:
			continue
		# Grab code from smsreceivefree.com
		gmail_page.get_code()

		gmail_page.submit_code()
		gmail_page.fill_in_info()
		gmail_page.confirm_rules()
		user_number += 1
	#gmail_page.quit()