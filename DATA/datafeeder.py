#!/usr/bin/python3.7
# -*-coding:utf-8 -
"""File Get the data in your DB MySQL"""

import random

from DATA.datamanager import DataManager

class DataFeeder:
    """class datafeeder"""
    def __init__(self):
        """Initializing"""
        self.data_manager = DataManager()

    def get_substitutes_list(self):
        """ substitutes mysql"""
        query_sub_list = """SELECT Products.product_name AS nom
        FROM Substitutes
        INNER JOIN Products
            ON Substitutes.substitute_id = Products.id """
        self.data_manager.cursor.execute(query_sub_list)
        substitutes = self.data_manager.cursor.fetchall()
        return substitutes

    def get_categories(self):
        """ categories in the database """
        query_cat = """SELECT name FROM Categories"""
        self.data_manager.cursor.execute(query_cat)
        categories = self.data_manager.cursor.fetchall()
        categories_list = list()
        for i in categories:
            categories_list.append(str(i[0]))
        categories_list = random.sample(categories_list, 10)
        return categories_list

    def get_products(self, category):
        """ products for a category """
        query_prod = """SELECT Products.product_name AS nom
        FROM Products
        INNER JOIN categories
            ON Products.category_id = Categories.id
        where Categories.name = '%s' """ % category
        self.data_manager.cursor.execute(query_prod)
        try:
            products = self.data_manager.cursor.fetchall()
            products_list = list()
            for i in products:
                products_list.append(str(i[0]))
            products_list = random.sample(products_list, 5)
            return products_list
        except ValueError:
            print("Il n'y a pas de produits dans cette catégorie")
        return None

    def get_product_nutriscore(self, product):
        """ nutriscore of product """
        query_prod = """SELECT Products.nutriscore_grade
                FROM Products
                Where Products.product_name = '%s' """ % product
        self.data_manager.cursor.execute(query_prod)
        products = self.data_manager.cursor.fetchall()
        product_nutriscore = str(products[0][0])
        return product_nutriscore

    def get_substitutes(self, category, nutriscore_product):
        """ nustricore grade """
        query_sub = """SELECT Products.product_name AS nom,
        Products.description AS Description,
        Products.store AS Magasin,
        Products.url_product AS Lien
        FROM Products
        INNER JOIN Categories
            ON Products.category_id = Categories.id
        where Categories.name = '%s'
        AND Products.nutriscore_grade < '%s' """ \
                    % (category, nutriscore_product)
        self.data_manager.cursor.execute(query_sub)
        try:
            substitutes = self.data_manager.cursor.fetchall()
            substitutes_list = list()
            for i in substitutes:
                substitutes_list.append(str(i))
            substitute = random.sample(substitutes_list, 1)
            substitute = substitute[0].split(""", '""")
            return substitute
        except ValueError:
            print("Il n'y a pas de substitut pour votre produit")
        return None

    def record_substitutes(self, sub_name, product_name):
        """databaseDE"""
        query_sub = """INSERT INTO Substitutes (product_id, substitute_id)
         VALUES (
         (SELECT id
         FROM Products
         WHERE Products.product_name = '%s'),
         (SELECT id
         FROM Products
         WHERE Products.product_name = '%s'));""" % (product_name, sub_name)
        self.data_manager.cursor.execute(query_sub)
        print("Inserted", self.data_manager.cursor.rowcount, "row(s) of data.")
        self.data_manager.conn.commit()

    def get_record_substitutes(self):
        """substitutes recorded"""
        subs = self.get_substitutes_list()
        if subs:
            print("\n La liste de mes aliments substitués : ")
            subs_list = list()
            for i in subs:
                subs_list.append(str(i[0]))
            for count, elt in enumerate(subs_list):
                print("{} - {}".format(count + 1, elt))
        else:
            print("Vous n'avez pas encore de substitut")

    def quit_database(self):
        """Close mysql"""
        self.data_manager.conn.close()
