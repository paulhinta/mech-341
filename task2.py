from gc import collect
import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
from enthalpy import enthalpy, enthalpy_function
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
     return (10**(8.14019 - (1810.94)/(T + 244.485 -273.15)))*133.322  - 101300*(1-p)     #converted to Pa
# def P_dal(p, T):
#     return (10**(8.07131 - (1730.63)/(T + 233.4 -273.15)))*133.322  - 101300*(1-p)     #converted to Pa

g = P_dal(p, T)          #1 atm
h = h_f(p, T)
k = (g, h)

solution = nsolve(k, (p, T), (0.14, 373))

print("Equivalence ratio:  " + str(solution[0]) + ", Temperature (K): " + str(solution[1]))