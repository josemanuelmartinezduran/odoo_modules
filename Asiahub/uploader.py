# -*- coding: utf-8 -*-
import urllib
import json
import httplib

serviceurl = "https://sandboxcbt.mercadolibre.com/api/categories/1025"
response = urllib.(serviceurl)
print(response)

product = {
"SKU": "01428510",
"primary_variation_sku":  "Optional  primary variation SKU",
"product_type”: “women sunglass",
"product_title_english": "Product title in English",
"product_title_spanish": "Optional product title in Spanish",
"product_title_portuguese": "Optional product title in Portuguese",
"description_english": "Description in English",
"description_spanish": "Optional description in Spanish",
"description_portuguese": "Optional description in Portuguese",
"specification_english": "Specification in English",
"specification_spanish": "Optional specification in Spanish",
"specification_portuguese": "Optional specification Portuguese",
"category_id": "MercadoLibre CBT category id for the product",
"brand": "Product brand name",
"model": "Product model name",
"image_url": "Product image URL (s) : ~^~ separated",
"video_url": "Optional Product video url",
"country_of_origin": "Product country of origin",
"shipping_from": "Shipping from country",
"UPC": "optional UPC of product",
"currency": "Product price currency",
"sale_price": "Product sale price",
"quantity": "Product quantity",
"merchant_shipping_cost": "Product shipping cost",
"international_shipping_cost": 15.00,
"international_shipping_cost_by_country" : {"BR": 10.00, "MX": 12.00},
"estimated_delivery_time": "Estimated delivery time of the product",
"weight_unit": "Weight unit lb. or kg",
"package_weight": "Product package weight",
"dimension_unit": "Dimesion unit in or cm",
"package_width": "Product package width",
"package_height": "Product package height",
"package_length": "Product package length",
"condition": "New",
"warranty_english": "Warranty details in English",
"warranty_spanish": "Warranty details in Spanish",
"warranty_portuguese": "Warranty details in Portuguese",
"translation_required": "Optional,  1 (true default) / 0 (false)",
"variation":[{ "id":"33000", "value_id":"43000"}, {"id":"33002","value_id": "43000"}],
"is_primary_variation": 0}