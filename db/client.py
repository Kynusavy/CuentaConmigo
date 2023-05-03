from pymongo import MongoClient

#Conexion de base de datos local
#db_client = MongoClient().local

#Conexio desde base de datos remota en produccion (Mongo_Atlas)
db_client = MongoClient("mongodb+srv://jonavila:Jonavila.2023@cluster0.ehhbcgq.mongodb.net/?retryWrites=true&w=majority").test
