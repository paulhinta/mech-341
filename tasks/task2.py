import sys
sys.path.append('../')               #allow imports from one directory up

from gc import collect
import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
from functions.enthalpy import enthalpy, enthalpy_function
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
'''
al      = collection.find_one({"index":4})
h2o_l   = collection.find_one({"index":9})
al2o3   = collection.find_one({"index":0})
h2      = collection.find_one({"index":7})
h2o_g   = collection.find_one({"index":10})

T = sp.Symbol("T")      #temp
p = sp.Symbol("p")      #phi

#enthalpy of formation of general eqn
def h_f(p, T):
    #return p*al2o3["hf0 [J/mol]"] + 3*p*h2["hf0 [J/mol]"] + 3*(1-p)*h2o_g["hf0 [J/mol]"] - 3*h2o_l["hf0 [J/mol]"] - 2*p*al["hf0 [J/mol]"]
    return p*enthalpy_function(al2o3,T) + 3*p*enthalpy_function(h2,T) + 3*(1-p)*enthalpy_function(h2o_g,T) - 3*h2o_l["hf0 [J/mol]"] - 2*p*al["hf0 [J/mol]"]

#Take constants for 99-374 Celsius bc water needs to be vapour (i.e. can't be low temp)
#Dalton's Law: (n mol H2O/n mol gas)* P = Antoine's Law
def P_dal(p, T):
     return (10**(8.14019 - (1810.94)/(T + 244.485 -273.15)))  - 760*(1-p)     #760 mmHg = 1 atm

#use lower values
def P_dal_low(p, T):
    return (10**(8.07131 - (1730.63)/(T + 233.426 -273.15)))  - 760*(1-p)

#2 equations in phi, T
eqn1 = P_dal(p, T)      #Equation 1: equalizing the pressure via Dalton & Antoine
eqn2 = h_f(p, T)        #Equation 2: enthalpy equation
eqn3 = P_dal_low(p,T)
eqns = (eqn1, eqn2)
eqns_alt = (eqn3, eqn2)

solution = nsolve(eqns, (p, T), (0.5, 373))
alternate_solution = nsolve(eqns, (p, T), (0.5, 373))

collection=db['q2']

collection.update_one({"index":0}, {"$set": {"Equivalence Ratio":float(solution[0]), "Equivalence Ratio (Alternate)":float(alternate_solution[0])}}, upsert=True)
collection.update_one({"index":1}, {"$set": {"Temperature [K]":float(solution[1]), "Temperature (Alternate) [K]":float(alternate_solution[1])}}, upsert=True)

#place in a collection for analysis in question 8
collection=db['q8']
collection.update_one({"index":0}, {"$set": {"Equivalence Ratio":float(solution[0]), "Temperature [K]": float(solution[1])}}, upsert=True)