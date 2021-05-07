#!/usr/bin/python3.7
# -*-coding:utf-8 -

import mysql.connector

mybd = mysql.connector.connect(
    host="localhost",
    user="purebeure",
    password="pure",
    database="pure_beure"
)
print(mybd)
