'''Arquivo onde a conexão com banco de dados é feita'''

import pymysql

bancoBT = pymysql.connect(host="localhost", port=3306,
                          user='root', passwd='', database='beautytime')
