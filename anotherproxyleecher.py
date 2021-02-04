from json import JSONDecoder
import requests
from lxml import html
import sys
import re
import base64

def cybersyndrome():
	try:
		proxies = []

		res = requests.get('http://www.cybersyndrome.net/plr5.html')
		doc = html.fromstring(res.content)
		rows = doc.find('.//table').findall('.//tr')

		for row in rows[1:]:
			proxies.append(row[1].text.strip())

		return proxies
	except Exception as ex:
		return False

def aliveproxy_(url):
	try:
		res = requests.get(url)
		proxies = []

		doc = html.fromstring(res.content)
		rows = doc.findall('.//table')[1][0][1][0]

		for row in rows[1:]:
			proxies.append(row[0].text.strip())

		return proxies
	except Exception as ex:
		return []

def aliveproxy():
	try:
		proxies = []

		proxies += aliveproxy_('http://aliveproxy.com/high-anonymity-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/anonymous-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/us-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/ru-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/jp-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/ca-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/fr-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/gb-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/de-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/com-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/net-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/org-proxy-list/')
		proxies += aliveproxy_('http://aliveproxy.com/edu-proxy-list/')

		return proxies
	except Exception as ex:
		return False

def proxz_(url):
	res = requests.get(url)
	return re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+',res.content.decode())

def proxz():
	try:
		proxies = []

		proxies += proxz_('http://www.proxz.com/proxy_list_high_anonymous_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_anonymous_us_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_uk_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_jp_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_ca_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_port_std_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_port_nonstd_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_cn_ssl_0.html')
		proxies += proxz_('http://www.proxz.com/proxy_list_fr_0.html')
		
		return proxies
	except Exception as ex:
		return False

def proxybunker():
	try:
		for i in range(2,6):
			try:
				return list(set(requests.get(f'https://proxy-bunker.com/api{i}.php').text.strip().splitlines()))
			except:
				continue
		return []
	except Exception as ex:
		return False

def proxyscrape():
	try:
		return requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&country=US&anonymity=elite&ssl=yes').text.strip().splitlines()
	except Exception as ex:
		return False

def freeproxylist_(url):
	try:
		proxies = []

		res = requests.get(url)
		doc = html.fromstring(res.content)

		for table in doc.findall('.//table'):
			if 'id' in table.attrib and table.attrib['id'] == 'proxylisttable':
				rows = table.find('.//tbody').findall('.//tr')
				for row in rows:
					if len(row) > 5:
						proxyType = row[4].text.strip()
						if 'elite' in proxyType or 'anonymous' in proxyType or 'level3' in proxyType:
							proxies.append(row[0].text.strip() + ":" + row[1].text.strip())

		return proxies
	except Exception as ex:
		return False

def freeproxylist():
	return freeproxylist_("https://free-proxy-list.net/")

def sslproxies():
	return freeproxylist_("https://sslproxies.org/")

def freeproxylists():
	def getPage(doc):
		print(doc)
		proxies = []

		for table in doc.findall('.//table'):
			print(table)
			if 'class' in table.attrib and table.attrib['class'] == 'DataGrid':
				print('finded : ',table)
				rows = table.findall('.//tr')
				print(rows)
				for row in rows:
					print(row,row.attrib)
					if 'class' in row.attrib and row.attrib['class'] != "Caption" and len(row.findall('.//td')) > 2:
						print('row : ',row)
						proxies.append(html.fromstring(urllib.parse.unquote(re.findall(r'IPDecode\((?:\'|\")(.*)(?:\'|\")\)',row[0][0].text)[0])).text + ":" + row[1].text)
		return proxies

	try:
		proxies = []

		res = requests.get("http://www.freeproxylists.net/?c=&pt=&pr=HTTP&a[]=2&u=0")
		doc = html.fromstring(res.content)
		proxies += getPage(doc)

		pages = doc.find('.//div[@class="page"]')
		if pages:
			pagelinks = list(set(list(map(lambda x:x.attrib['href'],pages.findall('.//a')))))
			for link in pagelinks:
				if not link.startswith('http'):
					link = "http://www.freeproxylists.net/" + link
				proxies += getPage(html.fromstring(requests.get(link).content))

		return proxies

	except Exception as ex:
		return False

def freeproxycz_(url):
	def getPage(doc):
		proxies = []

		#document.write(Base64.decode("NTQuMjM2LjI1My4xMjk="))
		for table in doc.findall('.//table'):
			if 'id' in table.attrib and table.attrib['id'] == 'proxy_list':
				rows = table.find('.//tbody').findall('.//tr')
				for row in rows:
					if len(row.findall('.//td')) > 2:
						# print(html.tostring(row))
						proxies.append(base64.b64decode(bytes(re.findall(r'document\.write\(Base64\.decode\((?:\"|\')(.+)(?:\"|\')\)\)',row[0][0].text or row[0][1].text)[0].encode())).decode() + ":" + row[1][0].text) 
		return proxies
	try:
		proxies = []

		res = requests.get(url)
		doc = html.fromstring(res.content)
		pagelinks = list(set(list(map(lambda x:"http://free-proxy.cz/"+x.attrib['href'],doc.find('.//div[@class="paginator"]').findall('.//a')))))

		proxies += getPage(doc)

		for link in pagelinks:
			proxies += getPage(html.fromstring(requests.get(link).content))

		return proxies
	except Exception as ex:
		return []

def freeproxycz():
	proxies = []

	proxies += freeproxycz_("http://free-proxy.cz/en/proxylist/country/all/http/ping/level1")
	proxies += freeproxycz_("http://free-proxy.cz/en/proxylist/country/all/https/ping/level1")

	return list(set(proxies))

def proxynova():	
	try:
		proxies = []

		res = requests.get('https://www.proxynova.com/proxy-server-list/elite-proxies/')
		doc = html.fromstring(res.content)		

		for table in doc.findall('.//table'):
			if 'id' in table.attrib and table.attrib['id'] == 'tbl_proxy_list':
				rows = table.find('.//tbody').findall('.//tr')
				for row in rows:
					if 'data-proxy-id' in row.attrib:
						print(html.tostring(row))
						proxies.append(re.findall(r'document.write\((?:\'|\")(.*)(?:\'|\")\)',row[0][0][0].text.strip())[0] + ":" + row[1].text.strip())


		return proxies
	except Exception as ex:
		return False


def proxyscan():
	try:
		proxies = []

		cookies = requests.get('https://www.proxyscan.io/').cookies

		res = requests.post('https://www.proxyscan.io/Home/FilterResult',data='status=1&ping=&selectedType=HTTP&selectedType=HTTPS&SelectedAnonymity=Anonymous&SelectedAnonymity=Elite&sortPing=false&sortTime=true&sortUptime=false',cookies=cookies)
		rows = html.fromstring(res.content)

		for row in rows:
			if 'HTTP' in row[4].text.strip() and "OK" in row[7][0].text.strip():
				proxies.append(row[0].text.strip() + ":" + row[1].text.strip())

		return proxies
	except Exception as ex:
		return False


def checkerproxy():
	def getArchive(data):
		data = JSONDecoder().decode(data)

		proxies = []

		for item in data:
			if (item['type'] == 1 or item['type'] == 2) and item['kind'] == 2:
				proxies.append(item['addr'])

		return proxies

	try:
		proxies = []

		res = requests.get('https://checkerproxy.net/')
		doc = html.fromstring(res.content)

		links = doc.findall('.//a')
		for link in links:
			print(link.attrib['href'])
			if 'href' in link.attrib and (link.attrib['href'].startswith('/archive') or link.attrib['href'].startswith('archive')):
				proxies += getArchive(requests.get('https://checkerproxy.net/api'+link.attrib['href']).text)

		return list(set(proxies))
	except Exception as ex:
		return False

apis = {
	'cybersyndrome':cybersyndrome,
	'aliveproxy':aliveproxy,
	'proxz':proxz,
	'proxybunker':proxybunker,
	'proxyscrape':proxyscrape,
	'freeproxylist':freeproxylist,
	'sslproxies':sslproxies,
	# 'freeproxylists':freeproxylists,
	'freeproxycz':freeproxycz,
	'proxynova':proxynova,
	'proxyscan':proxyscan,
	'checkerproxy':checkerproxy
}

def getProxies():
	proxies = []

	for name,api in apis.items():
		pp = api()
		if pp:
			proxies += pp
	return proxies

if __name__ == "__main__":

	proxies = getProxies()
	open('proxies.txt','w').write('\n'.join(proxies))
