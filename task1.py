import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
import sympy as sp
import numpy as np

#from calc_hf import calc            #side function to calculate hf

load_dotenv()

pw = os.getenv("PASSWORD")          #fetch pw from environment

#mongo connection string
connect = "mongodb+srv://paulhinta:" + pw + "@cluster0.p3kas.mongodb.net/inputs?retryWrites=true&w=majority&ssl=true" 

ca = certifi.where()                #mongo connection certificate
client = pymongo.MongoClient(connect, tlsCAFile=ca)
db = client['inputs']               #database that we are using
collection=db['selected-data']      #connection that we are using
cursor = collection.find({"Specie": "H2O"})  #get H2

#THERMO STUFF STARTS HERE

#declare variables of integration
x = sp.Symbol("x")
T = sp.Symbol("T")

#first function for cp; water vapour < 1000K
def f(x):
    return cursor[0]["a1"]*x**-2 + cursor[0]["a2"]*x**-1 + cursor[0]["a3"] + cursor[0]["a4"]*x + cursor[0]["a5"]*x**2 + cursor[0]["a6"]*x**3 + cursor[0]["a7"]*x**4

#compute upper & lower limits of integration
int_f = sp.integrate(f(x),x)
lower_f = float(int_f.subs(x, 298))
upper_f = int_f.subs(x, T)
cp_Tf = upper_f - lower_f +8.314*cursor[0]["b1"]       ##symbolic representation of cp as f(T)
print(cp_Tf)

#second function for cp; water vapour > 1000K
def g(x):
    return cursor[1]["a1"]*x**-2 + cursor[1]["a2"]*x**-1 + cursor[1]["a3"] + cursor[1]["a4"]*x + cursor[1]["a5"]*x**2 + cursor[1]["a6"]*x**3 + cursor[1]["a7"]*x**4

#compute upper & lower limits of integration
int_g = sp.integrate(g(x),x)
lower_g = float(int_g.subs(x, 298))
upper_g = int_g.subs(x, T)
cp_Tg = upper_g - lower_g +8.314*cursor[1]["b1"]       ##symbolic representation of cp as f(T)
print(cp_Tg)





er = 0 #equivalence ratio
# while er <= 2:
#     print(er)
#     #print(calc({},{}))
#     x.append(er)
#     er += 0.02