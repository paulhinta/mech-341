import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
import sympy as sp
import numpy as np
from enthalpy import enthalpy       #function to calculate enthalpy

#from calc_hf import calc            #side function to calculate hf

load_dotenv()

pw = os.getenv("PASSWORD")          #fetch pw from environment

#mongo connection string
connect = "mongodb+srv://paulhinta:" + pw + "@cluster0.p3kas.mongodb.net/inputs?retryWrites=true&w=majority&ssl=true" 

ca = certifi.where()                #mongo connection certificate
client = pymongo.MongoClient(connect, tlsCAFile=ca)
db = client['inputs']               #database that we are using
collection=db['selected-data']      #connection that we are using

#THERMO STUFF STARTS HERE

#declare variables of math
p = sp.Symbol("p")

h2o = collection.find_one({"index":11})
o2 = collection.find_one({"index":13})
n2 = collection.find_one({"index":15})

#critical phi
p_t = p*enthalpy(h2o, 1000) + 3.76*enthalpy(n2, 1000) + (2-p)*enthalpy(o2, 1000)
p_base = sp.solve(p_t, p)
print(p_base)


er = 0 #equivalence ratio
