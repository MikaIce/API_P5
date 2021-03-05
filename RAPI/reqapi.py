#!/usr/bin/python3.5
# -*-coding:utf-8 -

import requests
import mysql.connector

def load_data(category):

    """fonction qui charge les données temporaire pour chaque categorie"""

    url_begin = 'https://fr.openfoodfacts.org/categorie'
    nb_page = 1
    url_end = 'json'
    #URL SYNTAX
    url = "{}/{}/{}.{}".format(url_begin, category, nb_page, url_page, url_end)

    response = requests.get(url)
    products = response.json()
     #How many page in a category.
    count = products["count"]
    loop = 3           # import only the tree first pages       #ceil(count/20) # 20 = pagination
    #fill database
    while loop > 0:
        #redefine url
        url = "{}/{}/{}.{}".format(url_begin, category, nb_page, url_end)

        response = requests.get(url)
        products = response.json()

        p_name = ""
        n_grade = ""
        cat_name = ""
        product = Product()
        for p in products["products"]:

            try:
                p_name = p["product_name_fr"]
                n_grade = p["nutrition_grades"]
                cat_name = p["pnns_groups_2"]
                url = p["url"]
            except KeyError: #to avoid empty field from OpenFoodFacts
                pass


            product.add(p_name, n_grade, cat_name, url, cursor)

        nb_page += 1
        loop -= 1

def fill_database():
    """Function which call a stored procedure in Database to fill table Product and Category"""

    stored_proc_sql = ("CALL fill_database()")
    cursor.execute(stored_proc_sql)

if __name__ == "__main__":

    #Define the connexion
    cnx = mysql.connector.connect(user="purebeure", password= "pure", database="alimentation")
    cursor = cnx.cursor()
    load_data("fruits-secs")
    load_data("produits-a-tartiner")
    load_data("cones-et-batonnets-surgeles")
    load_data("sandwichs")
    load_data("pizzas-et-tartes-surgelees")
    load_data("gateaux")
    load_data("jambons-de-paris")

    #fill table with datas
    try:
        fill_database()
    except mysql.connector.errors.IntegrityError:
        pass
    #make sure to commit data to database
    cnx.commit()
    #close connexion
    cursor.close()
    cnx.close()
