import sys
sys.path.append('../')               #allow imports from one directory up

import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
import numpy as np
from functions.enthalpy import enthalpy, aft_t1       #function to calculate enthalpy, adiabatic flame temp
import matplotlib.pyplot as plt

#FILLS UP THE MONGODB WITH data for question 1, it can easily be accessed by running analysis.py

#from calc_hf import calc            #side function to calculate hf

load_dotenv()

pw = os.getenv("PASSWORD")          #fetch pw from environment

#mongo connection string
connect = "mongodb+srv://paulhinta:" + pw + "@cluster0.p3kas.mongodb.net/inputs?retryWrites=true&w=majority&ssl=true" 

ca = certifi.where()                #mongo connection certificate
client = pymongo.MongoClient(connect, tlsCAFile=ca)
db = client['inputs']               #database that we are using
collection=db['q8']      #connection that we are using
'''
THERMO STUFF STARTS HERE
'''
#list of equivalence ratios & T_AD so we can plot them later
phi=[0]
T = [298.15]

#get all the phi and T and append them to the lists
for document in collection.find():
    phi.append(document["Equivalence Ratio"])
    T.append(document["Temperature [K]"])

plt.plot(phi, T, '-o')
plt.title("AFT vs Equivalence Ratio for the oxidation of Al with water")
plt.ylabel("Adiabatic Flame Temperature [K]")
plt.xlabel("Equivalence Ratio [-]")
plt.xticks(np.arange(0,1.6,step=0.3))
plt.show()
