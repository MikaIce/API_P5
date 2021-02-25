#! /usr/bin/#!/usr/bin/env python3
# coding: utf-8

import requests

payload = {"search_terms": "Lindt",
            "search_tag": "brands",
            "sort_by": "unique_scans_n",
            "page_size": 50,
            "json": 1}
res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)

results = res.json()
products = results["products"]

for product in products:
    print(product["product_name"])
