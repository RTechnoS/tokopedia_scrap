

#########################################
#		CODE FROM @rusman_toby			#
#		rusmants.public@pm.me 			#
#	  http://github.com/rtechnos		#
#########################################


import requests, json, os
from bs4 import BeautifulSoup as bs
from pandas import DataFrame

class tokopedia():

	def __init__(self, store, saveType=1):
		self.urlStore = 'https://tokopedia.com/'+store
		self.store = store
		self.saveType=saveType
		self.headerbrowser = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
		print(self.urlStore)
		self.getid()
	
	def getid(self):
		try:
			req = requests.post(self.urlStore, headers=self.headerbrowser, timeout=3.000)
			print(req.status_code)
			if req.status_code == 200:
				print(req)
				sup = bs(req.text, 'html.parser')
				for i in sup.find_all('meta', attrs={'name':'branch:deeplink:$android_deeplink_path'}):
					self.idToko = i.get('content')[5:]
					print('id Toko : '+self.idToko)
				self.scrapJson()
			else:
				print('Toko Tidak ditemukan')
		except:
			print('Toko tidak valid')
	def scrapJson(self):
		urlJson = 'https://ace.tokopedia.com/search/product/v3?shop_id={}&rows=80&start=0&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=shop_product'.format(self.idToko)
		req = requests.get(urlJson, headers=self.headerbrowser)
		self.hasilReq = req.json()
		if not os.path.isdir(self.store):
			os.mkdir(self.store)
		with open('{}/{}_[detail].json'.format(self.store,self.store), 'w') as fileW:
			json.dump(self.hasilReq, fileW)
		self.showData()

	def showData(self):
		self.jumlahProduk = len(self.hasilReq['data']['products'])
		self.fullProduk = []
		print('Jumlah Produk Yang dijual : '+str(self.jumlahProduk))
		for num,i in enumerate(self.hasilReq['data']['products']):
			print('''{}. {}
Name : {}
Price : {}
Url : {}
Image_url : {}
Catagory_name : {}
'''.format(num+1,'-'*40,i['name'],  i['price'], i['url'], i['image_url'], i['category_name']))

			self.fullProduk.append([i['name'],i['price'],i['url'],i['image_url'],i['category_name']])
			#[{'name':i['name'], 'harga':i['price'], 'link':i['url'], 'image':i['image_url'],'category':i['category_name']}]
		self.saveProduk()

	def saveProduk(self):

		if self.saveType == 1:
			data = []
			for i in self.fullProduk:
				data += [{'name':i[0], 'price':i[1], 'url':i[2], 'image_url':i[3],'category_name':i[4]}]

			with open('{}/{}_[produk].json'.format(self.store,self.store), 'w') as fileW:
				json.dump(data, fileW)

		elif self.saveType == 2:
			try:
				df = DataFrame(self.fullProduk, columns=['name','price','url','image_url','category_name'])
				df.to_csv('{}/{}_[produk].csv'.format(self.store,self.store), index=False)
			except:
				logging.exception('[Error] save to csv')
				
			


inputLink = input('Nama Toko : https://tokopedia.com/')
print("\n1. Json\n2. CSV")

saveType = int(input('Select format save : '))
if saveType in [1,2]:
	actionToko = tokopedia(inputLink,saveType)
else:
	print("[Error] Select format save")



