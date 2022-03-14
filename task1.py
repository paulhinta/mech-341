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

#declare variables of math
p = sp.Symbol("p")

#fetch the species data from the db
h2o_1000 = collection.find_one({"index":10})
o2_1000 = collection.find_one({"index":12})
n2_1000 = collection.find_one({"index":14})

#critical point phi:
g = 2*p*enthalpy(h2o_1000, 1000) + 3.76*enthalpy(n2_1000, 1000) + 2*(1-p)*enthalpy(o2_1000, 1000)
p_crit = sp.solve(g, p)[0]

ers = []
afts = []

er = 0 #equivalence ratio

#fuel rich species
fr_h2o = collection.find_one({"index":11})   #h2o
fr_n2 = collection.find_one({"index":15})   #n2
fr_h2 = collection.find_one({"index":8})    #h2

#fuel lean case 1, er >= p_crit
f1_h2o = fr_h2o                             #h2o, same conditions as fuel rich
f1_n2 = fr_n2                               #n2, same conditinos as fuel rich
f1_o2 = collection.find_one({"index":13})                             #o2 instead of h2, use value at 1000K

#fuel lean case 2, er < p_crit -> use values from before (species 10, 12 14)

T_aft = 0       #adiabatic flame temp (dynamic variable)

#compute AFT
while True:
    if er > 2:
        break

    #fuel rich case
    if er >= 1:
        T_aft = aft(fr_h2o, fr_n2, fr_h2, er)
    
    #fuel lean, er > p_crit case
    elif er >= p_crit:
        T_aft = aft(f1_h2o, f1_n2, f1_o2, er)

    #fuel lean, er < p_crit case
    else:
        T_aft = aft(h2o_1000, n2_1000, o2_1000, er)

    afts.append(float(T_aft))
    ers.append(er)
    er += 0.02

#connect to the database and load data into the question 1 collection
collection = db['q1']
collection.update_one({"index":0}, {"$set": {"Axis":"X", "Data":ers}}, upsert=True)
collection.update_one({"index":1}, {"$set": {"Axis":"Y", "Data":afts}}, upsert=True)