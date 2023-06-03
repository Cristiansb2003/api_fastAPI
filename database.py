from peewee import MySQLDatabase

database = MySQLDatabase('fastapi_project',
                          user='root', 
                          password= 'admin', 
                          host='localhost',
                          port=3306)