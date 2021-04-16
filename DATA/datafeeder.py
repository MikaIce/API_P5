#!/usr/bin/python3.5
# -*-coding:utf-8 -

import random

from datamanager import DataManager

class DataFeeder:

    def __init__(self):

        self.data_manager = DataManager()

    def get_substitutes_list(self):

        query_sub_list = """SELECT Product.product_name AS nom
        FROM Substututes
        INNER JOIN Products
            ON Substitutes.substitute_id = Products_id """
        self.data_manager.cursor.execute(query_sub_list)
        Substitutes = self.data_manager.cursor.fetchall()
        return substitutes

    def get_categories(self):

        query_cat = """SELECT name FROM Categories"""
        self.data_manager.cursor.execute(query_cat)
        Categories = self.data_manager.cursor.fetchall()
        categories_list = list()
        for i in categories:
            categories_list.append(str(i[0]))
        categories_list = random.sample(categories_list, 10)
        return categories_list

    def get_products(self, category):

        query_prod = """SELECT Products.product_name AS nom
        FROM Products
        INNER JOIN categories
            ON Products.category_id = Categories.id
        where Categories.name = '%s' """ % category
        self.data_manager.cursor.execute(query_prod)
        try:
