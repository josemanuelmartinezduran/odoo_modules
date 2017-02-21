import urllib
import urllib2
import base64
import json


def get_products(out_csv_products):

	f_products_csv = open(out_csv_products, "w")

	product_offset=0
	product_limit=300
	n_rows=1

	while product_offset<n_rows:
		url = "https://desenvolvedores.cnova.com/api-portal/proxy/api/v2/loads/products?_offset="+str(product_offset)+"&_limit="+str(product_limit)
		headers = {"client_id" : "7jspqddwKW8M", "access_token" : "sOjBL60bKo3a"}

		request = urllib2.Request(url)
		request.add_header('Content-Type', 'application/json')
		request.add_header('Accept', 'application/json')

		for key,value in headers.items():
		  request.add_header(key,value)

		try:
		     response = urllib2.urlopen(request)
		     print response.info().headers
		     print "\n"
		     print request.header_items()
		     #print response.read()

		except urllib2.HTTPError as e:
		     print e.code
		     print e.read() 

		product_list = response.read()
		off = 0
		str_find = "\"href\":\"/loads/products/"

		while off<len(product_list):
			off = product_list.find(str_find,off)
			off_id =  product_list.find("\"",off+len(str_find))
			sku_id =  product_list [off+len(str_find):off_id] 
			if off<0:
				break
			off = off+1
			print sku_id
			f_products_csv.write (sku_id)
			f_products_csv.write ("\n")
			

		str_find = "\"totalRows\",\"value\":\""
		off_n = product_list.find(str_find)
		off_total =  product_list.find("\"",off_n+len(str_find))
		n_rows =  int(product_list [off_n+len(str_find):off_total])
		#print "total: " + str(n_rows)
		product_offset = product_offset+product_limit



