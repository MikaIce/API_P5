#!/usr/bSSin/python3.7
# -*-coding:utf-8 -
"""File Menu pure beurre for user"""

import sys

from DATA.datafeeder import DataFeeder
from DATA.datamanager import DataManager
from SQL.dbcreator import DBCreator

class MenuHandler:
    """Menu"""
    def __init__(self):

        self.continue_main_menu = True
        self.continue_choose_category = True
        self.continue_choose_product = True
        self.continue_choose_substitute = True
        self.continue_record_substitute = True
        self.continue_cat_menu = True
        self.continue_prod_menu = True
        self.data_feeder = DataFeeder()

    def show_main_menu(self):
        """Start"""
        while self.continue_main_menu:
            print("""
            ###################################################
            # Pure Beurre vous propose les options suivantes  #
            #                                                 #
            # 1.Quel aliment souhaitez-vous remplacer ?       #
            # 2.Retrouver mes aliments substitués             #
            #                                                 #
            # 3.Exit/Quit                                     #
            ###################################################
            """)
            try:
                ans = input("Que voulez-vous faire ? ")
                if ans == "1":
                    self.continue_cat_menu = True
                    self.continue_main_menu = False
                    self.show_category_menu()
                elif ans == "2":
                    self.data_feeder.get_record_substitutes()
                elif ans == "3":
                    self.data_feeder.quit_database()
                    print("\n Au revoir")
                    sys.exit()
                elif ans != "":
                    print("\n Ce n'est pas un choix valide")
            except ValueError:
                print("Veuillez entrer un nombre valide")

    def show_category_menu(self):
        """ Menu categories"""
        while self.continue_cat_menu:
            print("""
            ###################################################
            # Pure Beurre vous propose les options suivantes  #
            #                                                 #
            # 1.Sélectionner une catégorie                    #
            # 2.Retourner au menu principal                   #
            #                                                 #
            ###################################################
            """)
            try:
                ans = input("Que voulez-vous faire ? ")
                if ans == "1":
                    print("\n La liste des catégories: \n")
                    self.continue_main_menu = False
                    self.continue_cat_menu = False
                    self.continue_choose_category = True
                    self.choose_category()
                elif ans == "2":
                    self.continue_main_menu = True
                    self.show_main_menu()
                elif ans != "":
                    print("\n Ce n'est pas un choix valide")
            except ValueError:
                print("Veuillez entrer un nombre valide")

    def choose_category(self):
        """Catagory"""
        while self.continue_choose_category:
            try:
                cat_list = self.data_feeder.get_categories()
                for count, element in enumerate(cat_list):
                    print("{} - {}".format(count + 1, element))
                ans = input("\n Veuillez choisir une catégorie dans "
                            "la liste ci-dessus : ")
                ans = int(ans)
                if ans in range(1, len(cat_list) + 1):
                    print("Vous avez choisi la catégorie : "
                          "{}".format(cat_list[ans - 1]))
                    category_choose = cat_list[ans - 1]
                    self.continue_prod_menu = True
                    self.continue_choose_category = False
                    self.show_product_menu(category_choose)
                elif ans != "":
                    print("\nCe n'est pas un choix valide \n")
            except ValueError:
                print("Veuillez entrer un nombre valide")

    def show_product_menu(self, category):
        """Menu products"""
        while self.continue_prod_menu:
            print("""\n
            ###################################################
            # Pure Beurre vous propose les options suivantes  #
            #                                                 #
            # 1.Sélectionner un produit                       #
            # 2.Retourner à la liste des catégories           #
            #                                                 #
            ###################################################
            """)
            try:
                ans = input("Que voulez-vous faire ? ")
                if ans == "1":
                    self.continue_prod_menu = False
                    self.continue_choose_product = True
                    self.choose_product(category)
                elif ans == "2":
                    self.continue_cat_menu = True
                    self.show_category_menu()
                elif ans != "":
                    print("\n Ce n'est pas un choix valide")
            except ValueError:
                print("Veuillez entrer un nombre valide")

    def choose_product(self, category):
        """Product"""
        while self.continue_choose_product:
            prod_list = self.data_feeder.get_products(category)
            if prod_list:
                for count, element in enumerate(prod_list):
                    print("{} - {}".format(count + 1, element))
                ans = \
                    input("Veuillez choisir un produit dans la "
                          "liste ci-dessus ")
                try:
                    ans = int(ans)
                    if ans in range(1, len(prod_list) + 1):
                        print("Vous avez choisi le produit : {} \n".format(
                            prod_list[ans - 1]))
                        product_choose = prod_list[ans - 1]
                        nutriscore_produit = self.data_feeder.\
                            get_product_nutriscore(product_choose)
                        print("Le nutriscore associé à votre produit est de {}"
                              .format(nutriscore_produit))
                        self.continue_choose_product = False
                        self.continue_choose_substitute = True
                        self.choose_substitute(category, nutriscore_produit,
                                               product_choose)
                    elif ans != "":
                        print("\n Ce n'est pas un choix valide")
                except ValueError:
                    print("Veuillez entrer un nombre valide")
            else:
                self.continue_choose_category = True
                self.continue_choose_product = False
                self.choose_category()

    def choose_substitute(self, category, nutriscore, product_choose):
        """Menu substitute"""
        while self.continue_choose_substitute:
            sub = self.data_feeder.get_substitutes(category, nutriscore)
            if sub:
                print("Nous avons trouvé un substitut à votre produit"
                      " avec un meilleur nutriscore \n:")
                print("Nom : {} \n"
                      "Description : {} \n"
                      "Magasin : {} \n"
                      "Lien : {} \n".format(sub[0].replace("""('""", ""),
                                            sub[1].replace("'", ""),
                                            sub[2].replace("'", ""),
                                            sub[3].replace("""')""", "")))
                self.continue_choose_substitute = False
                self.continue_record_substitute = True
                self.record_substitute(sub[0], product_choose)
            else:
                self.continue_choose_substitute = False
                self.continue_main_menu = True

    def record_substitute(self, sub_name, product_name):
        """Menu record"""
        sub_name = sub_name.replace("""(\'""", "")
        sub_name = sub_name.replace("""\'""", "")
        while self.continue_record_substitute:
            ans = input("Voulez vous sauvegarder cet aliment dans "
                        " votre base de données ? (O/N) ")
            if ans == "O":
                self.data_feeder.record_substitutes(sub_name, product_name)
                print("\nL'aliment a été sauvegardé")
                self.continue_record_substitute = False
                self.continue_main_menu = True
                self.show_main_menu()
            elif ans == "N":
                print("\nL'aliment n'a pas été sauvegardé")
                self.continue_record_substitute = False
                self.continue_main_menu = True
                self.show_main_menu()
            elif ans != "":
                print("\nCe n'est pas un choix valide")
