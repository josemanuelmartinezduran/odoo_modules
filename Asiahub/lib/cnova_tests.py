#!/usr/bin/env python
# -*- coding: utf-8 -*-

from csv_pre import pre_process_csv
from put_products import put_products_fun
from load_products import get_products
from products_subset import get_subset_products

pre_process_csv ("../../data/CNOVA/CNOVAImport_Asiahub_Test50.csv","../../data/CNOVA/CNOVAImport_Asiahub_S1_final.csv")
put_products_fun("../../data/CNOVA/maptojson_cnova.txt", "../../data/CNOVA/CNOVAImport_Asiahub_S1_final.csv")
get_products("../../data/CNOVA/cnova_products.csv")
get_subset_products("../../data/CNOVA/CNOVAImport_Asiahub_S1_final.csv", "../../data/CNOVA/cnova_products.csv", "../../data/CNOVA/CNOVAImport_Asiahub_S1_final_sub.csv")
