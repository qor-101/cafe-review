from pymongo import MongoClient
import sqlite3

def func_upload(db_name,coll_name,doc):
    
    myclient = MongoClient('mongodb://localhost:27017/')
    db = myclient[db_name]
    collection = db[coll_name]
    result = collection.insert_one(doc)
    return result

def func_retreive(db_name,coll_name,key_dict):
    
    myclient = MongoClient('mongodb://localhost:27017/')
    db = myclient[db_name]
    collection = db[coll_name]
    list_docs = collection.find(key_dict)
    return list_docs

def func_update(db_name,coll_name,key_dict):
    
    myclient = MongoClient('mongodb://localhost:27017/')
    db = myclient[db_name]
    collection = db[coll_name]
    result = collection.update_one(key_dict)
    return result

def get_user():
    mydb = sqlite3.connect("db.sqlite3")
    mycursor = mydb.cursor()  
    res = mycursor.execute('SELECT username FROM auth_user')
    lis=[]
    for i in res:
        lis.append(i[0])
    mydb.close()
    return lis