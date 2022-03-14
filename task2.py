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

T = sp.Symbol("T", constant=False)      #temp
p = sp.Symbol("p")      #phi

#enthalpy of formation of general eqn
def h_f(p, T):
    return p*enthalpy_function(al2o3,T) + 3*p*enthalpy_function(h2,T) + 3*(1-p)*enthalpy_function(h2o_g,T) - 3*enthalpy_function(h2o_l,T) - 2*p*enthalpy_function(al,T)

#we need a second equation, thus we can use Antoine's relationship
#water vapour occurs at T > 100C -> so use the second temp relationship
def P_sat(T):
    return 10**(8.14019 - (1810.94)/(T + 244.45))

g = P_sat(T) - 760          #1 atm = 760 mmhg
t_sat = nsolve(g, 300)      #initial guess 300C (numerical solve)
t_sat = t_sat + 273.15      #saturation temp in K

h = h_f(p, t_sat)           #sub saturation temperature into the enthalpy equation

p_crit = sp.solve(h, p)     #find the critical ER

print(p_crit[0])            #p_crit ~ 0.227 for T_sat ~ 373 K
print(t_sat)