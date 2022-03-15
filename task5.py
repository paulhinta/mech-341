from gc import collect
import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
from enthalpy import enthalpy, aft_t5
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

governing stoich eqn: 2Al + 3H2O (l) -> Al2O3 + 3H2 + 3H2O (g)
Now, T = 2327K (Fully melted point of Al2O3)
'''
al      = collection.find_one({"index":5})
h2o_l   = collection.find_one({"index":9})
al2o3   = collection.find_one({"index":3})  #New properties of al2o3 @ 2373; Aluminium is still solid but starting to melt here
h2      = collection.find_one({"index":8})
h2o_g   = collection.find_one({"index":11})

T = sp.Symbol("T")                 
#enthalpy of formation of general eqn
#for liquid water, sub maximum temp 373.15K
#AFT as f(T)
f = aft_t5(al, h2o_l, al2o3, h2, h2o_g, T)

#numerical solution
sol = nsolve(f, 2327)

collection = db['q5']
collection.update_one({"index":0}, {"$set": {"AFT [K]":float(sol)}}, upsert=True)