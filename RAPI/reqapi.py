#! /usr/bin/#!/usr/bin/env python3
# coding: utf-8

import requests

res = requests.get("https://world.openfoodfacts.org/api/v0/product/3017620425400.json")

results = res.json()

results2 = results.keys()


product = results["product"]


print(res.status_code)
print(res.url)
print(product["categories"])
print(results2)
#nombre d'atribut du produit
print(len(product))
