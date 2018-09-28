import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://www.bitcoinabuse.com/reports?page={}"
MAX_PAGE = 20

REPORTS_URL = "https://www.bitcoinabuse.com/reports/{}?page={}"
MAX_REPORT_PAGE = 10
REPORT_KEYWORDS = ["exort","video","porn","$700"]

f = open("addresses.txt","w+")

def getPageAddresses(page):
	addresses = set()

	page_url = (PAGE_URL).format(page)
	page = requests.get(page_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	divs = soup.find_all('div',class_='mb-3')
	for div in divs:
		anchors = div.find('a')
		for anchor in anchors:
			addresses.add(anchor)
	print (("Addresses found on this page: {}").format(len(addresses)))
	return addresses

def addressReportsContainKeywords(address,keywords):
	reports = set()
	print (("Address: {}").format(address))
	current_reports_page = 1
	while current_reports_page < MAX_REPORT_PAGE:
		print (("Reports Page: {}").format(current_reports_page))
		page_url = (REPORTS_URL).format(address,current_reports_page)
		page = requests.get(page_url)
		if any(word in str(page.content) for word in keywords):
			print (('Address {}, at least one keyword found!!').format(address))
			return True
		current_reports_page = current_reports_page + 1

	print (('Address {}, keywords not found.').format(address))
	return False

filtered_addresses = set()

current_page = 1
while current_page < MAX_PAGE:
	print (("Addresses Page: {}").format(current_page))
	addresses = getPageAddresses(current_page)
	for address in addresses:
		if addressReportsContainKeywords(address,REPORT_KEYWORDS):
			filtered_addresses.add(address)
			f.write(address + "\n")
	current_page = current_page + 1

print (("Total addresses found: {}").format(len(filtered_addresses)))
print ("Check addresses.txt and enjoy!")



