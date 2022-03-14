import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
import sympy as sp
import numpy as np
from enthalpy import enthalpy, aft       #function to calculate enthalpy, adiabatic flame temp

#FILLS UP THE MONGODB WITH data for question 1, it can easily be accessed by running analysis.py

#from calc_hf import calc            #side function to calculate hf

load_dotenv()

pw = os.getenv("PASSWORD")          #fetch pw from environment

#mongo connection string
connect = "mongodb+srv://paulhinta:" + pw + "@cluster0.p3kas.mongodb.net/inputs?retryWrites=true&w=majority&ssl=true" 

ca = certifi.where()                #mongo connection certificate
client = pymongo.MongoClient(connect, tlsCAFile=ca)
db = client['inputs']               #database that we are using
collection=db['selected-data']      #connection that we are using

'''
THERMO STUFF STARTS HERE
'''
for i in range(0,16):
    x = collection.find_one({"index":i})
    if x["T_min [K]"] > 298:
        continue
    print(x["Specie"] + " " + str(x["index"]))
    print(enthalpy(x))
    print(x["hf0 [J/mol]"])
    print("***")