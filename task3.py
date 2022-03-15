from gc import collect
import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
from enthalpy import enthalpy
import sympy as sp
from sympy import nsolve

#FILLS UP THE MONGODB WITH data for question 1, it can easily be accessed by running analysis.py

#from calc_hf import calc            #side function to calculate hf

load_dotenv()

pw = os.getenv("PASSWORD")          #fetch pw from environment; environment variable to keep my info hidden lol

#mongo connection string
connect = "mongodb+srv://paulhinta:" + pw + "@cluster0.p3kas.mongodb.net/inputs?retryWrites=true&w=majority&ssl=true" 

ca = certifi.where()                #mongo connection certificate
client = pymongo.MongoClient(connect, tlsCAFile=ca)
db = client['inputs']               #database that we are using
collection=db['selected-data']      #connection that we are using

'''
THERMO STUFF STARTS HERE

governing stoich eqn: 2*phi*Al + 3H2O (l) -> phi*Al2O3 + 3*phi*H2 + 3*(1-phi)*H2O (g)
Now, T = 2327 (Melting point of Al2O3)
'''
al      = collection.find_one({"index":5})
h2o_l   = collection.find_one({"index":9})
al2o3   = collection.find_one({"index":2})  #New properties of al2o3 @ 2373; Aluminium is still solid but starting to melt here
h2      = collection.find_one({"index":8})
h2o_g   = collection.find_one({"index":11})

T = 2327                 #Melting point of Al2O3
p = sp.Symbol("p")      #phi

#enthalpy of formation of general eqn
#for liquid water, sub maximum temp 373.15K
def h_f(p, T):
    return p*enthalpy(al2o3,T) + 3*p*enthalpy(h2,T) + 3*(1-p)*enthalpy(h2o_g,T) - 3*h2o_l["hf0 [J/mol]"] - 2*p*al["hf0 [J/mol]"]

h = h_f(p, T)
sol = nsolve(h, 0.5)

print(sol)

collection = db['q3']
collection.update_one({"index":0}, {"$set": {"phi":float(sol)}}, upsert=True)