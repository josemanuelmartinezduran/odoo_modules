#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import base64
import json

def put_products_fun (map_file, data_file):

	fjson = open(map_file, "r")
	data_map = fjson.read()

	fcsv = open(data_file, "r")
	headers = fcsv.readline()
	headers = headers.replace("\n", "")

	splited_headers = headers.split (',')
	print splited_headers

	products = fcsv.readline()
	final_json = "[\n"

	while products:
		products = products.replace("\n", "")
		splited_products = products.split (',')

		product_json = data_map
	

		for x in range(0,len(splited_headers)):
			product_json = product_json.replace(splited_headers[x], splited_products[x])

		final_json = final_json + product_json
		products = fcsv.readline()
		if products:
			final_json = final_json + ",\n"
		else:
			final_json = final_json + "\n"
	
	final_json = final_json + "]\n"

	fjson = open("final_json.txt", "w")
	fjson.write (final_json)

	#print final_json
	#web service to upload

	#exit (1)	
	url = "https://desenvolvedores.cnova.com/api-portal/proxy/api/v2/loads/products"
	headers = {"client_id" : "7jspqddwKW8M", "access_token" : "sOjBL60bKo3a"}
	data = final_json;
	request = urllib2.Request(url)
	request.add_header('Content-Type', 'application/json')
	request.add_header('Accept', 'application/json')
	request.add_data(final_json)
	#jdata = json.dumps(data)

	for key,value in headers.items():
	  request.add_header(key,value)

	try:
	     response = urllib2.urlopen(request)
	     print response.info().headers
	     print "\n"
	     #print response.data()
	     print request.header_items()
	     print response.read()

	except urllib2.HTTPError as e:
	     print e.code
	     print e.read() 





