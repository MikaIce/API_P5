#!/usr/bin/python3.5
# -*-coding:utf-8 -

import mysql.connector
import openfoodfacts


class DataManager:

    def __init__(self):

        self.conn = mysql.connector.connect(host=CONNECTOR_HOST,
                                            user=CONNECTOR_USE,
                                            password=CONNECTOR_PASSWORD,
                                            database=CONNECTOR_DATABASE,
                                            auth_plugin='mysql_'
                                                        'native_password')
        self.cursor = self.conn.cursor()
        self.create_user = CREATE_USER
        self.create_db = CREATE_DB
        self.create_categories = CREATE_CATEGORIES
        self.create_products = CREATE_PRODUCTS
        self.create_substitutes = CREATE_SUBSTITUTES
        self.category_size = CATEGORY_SIZE
        self.cat_id = []
        self.cat_name = []

    def create_table(self, table):

        self.cursor.execute(table)

    def get_categories(self):

        categories = openfoodfacts.facets.get_categories()
        category_id = list()
        for i in categories:
            if "fr:" in i["id"]:
                category_id.append(i["id"])
        return category_id

    def get_id_categories(self):

        self.cursor.execute("""SELECT id FROM Categories""")
        products = sel.cursor.fetchall()
        id_categories = list()
        for t in products:
            id_categories.append(str(t[0]))
        return id_categories

    def insert_categories(self):

        self.cat_id = self.get_categories()
        if not self.get_id_categories():
            self.cat_name = [s.replace('fr:', '') for s in self.cat_id]
            i = 0
            while i < self.category_size:
                try:
                    query_cat = """INSERT INTO Categories (id, name)
                    VALUES ('%s','%s')""" % (self.cat_id[i], self.cat_name[i])
                    self.cursor.execute(query_cat)
                except:# pylint: disable=bare-except
                    continue
                i += 1
            self.insert_products()
        else:
            print("Votre base est a jour")

    def insert_products(self):

        id_categories = self.get_id_categories()
        for j in id_categories:
            products_list = openfoodfacts.products.get_by_category(j)
            for i in product_list:
                try:
                    query_prod = """INSERT INTO Products (id, category_id,
                    product_name, nutriscore_grade, store, url_product,
                    description) VALUES ('%s','%s','%s','%s','%s','%s','%s')
                    """ % (i["id"], "{}".format(j), i["product_name"],
                            i["nutriscore_grade"], i["stores"],
                            self.get_url_product(i["id"]), i["generic_name"])
                    self.cursor.execute(query_prod)
                except:# pylint: disable=bare-except
                    continue
