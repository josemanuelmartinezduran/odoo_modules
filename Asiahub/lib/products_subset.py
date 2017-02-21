import urllib
import urllib2
import base64
import json


def get_subset_products(in_csv_products, cnova_product_list, out_csv_products):

	fcsv = open(in_csv_products, "r")
	headers = fcsv.readline()
	headers = headers.replace("\n", "")

	splited_headers = headers.split (',')
	print splited_headers

	products_dict = {}
	products = fcsv.readline()

	while products:
		products = products.replace("\n", "")
		splited_products = products.split (',')
		#print splited_products[7]
		products = fcsv.readline()
		products_dict[splited_products[7]] = products

	#print products_dict

	fcsv = open(cnova_product_list, "r")
	cnova_product = fcsv.readline()

	while cnova_product:
		cnova_product = cnova_product.replace("\n", "")
		if cnova_product in products_dict:
			del products_dict[cnova_product]
		cnova_product = fcsv.readline()

	print products_dict
	print len(products_dict)
	
	f_products_csv = open(out_csv_products, "w")
	f_products_csv.write(headers)
	f_products_csv.write('\n')

	for product_info in products_dict:
	    	f_products_csv.write(products_dict[product_info])




