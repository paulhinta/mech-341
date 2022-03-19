from calendar import c
import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment
import matplotlib.pyplot as plt

load_dotenv()

pw = os.getenv("PASSWORD")          #fetch pw from environment

#mongo connection string
connect = "mongodb+srv://paulhinta:" + pw + "@cluster0.p3kas.mongodb.net/inputs?retryWrites=true&w=majority&ssl=true" 

ca = certifi.where()                #mongo connection certificate
client = pymongo.MongoClient(connect, tlsCAFile=ca)
db = client['inputs']               #database that we are using

'''
TASK 1 
'''
collection=db['q1']                 #connection that we are using

#Fetch q1 data from the database
x_axis = collection.find_one({"Axis":"X"})["Data"]
y_axis = collection.find_one({"Axis":"Y"})["Data"]

#Plot the question 1 data
plt.plot(x_axis, y_axis)
plt.title("AFT vs Equivalence Ratio for the combustion of H2 with air")
plt.ylabel("Adiabatic Flame Temperature [K]")
plt.xlabel("Equivalence Ratio [-]")
plt.show()
'''
TASK 2
'''
print("TASK 2")
collection=db['q2']
#Fetch q2 data from the database
print(
    "Considering the oxidation of aluminium with water and using the higher Antoine Coefficients, the equivalence ratio,phi, so that the produced water is saturated vapour is: phi = " + str(
        round(collection.find_one({"index":0})["Equivalence Ratio"],4)
    )
    + "\nThis occurs at a temperature, T: T = " + str(
        round(collection.find_one({"index":1})["Temperature [K]"],2)
    )
)
print(
    "Considering the oxidation of aluminium with water and using the lower Antoine Coefficients, the equivalence ratio,phi, so that the produced water is saturated vapour is: phi = " + str(
        round(collection.find_one({"index":0})["Equivalence Ratio (Alternate)"],4)
    )
    + "\nThis occurs at a temperature, T: T = " + str(
        round(collection.find_one({"index":1})["Temperature (Alternate) [K]"],2)
    )
)
'''
TASK 3
'''
print("TASK 3")
collection=db['q3']
print(
    "The equivalence ratio, phi, such that the aluminium oxide is just starting to melt (Fuel Lean Case): phi = " + str(
        round(collection.find_one({"index":0})["phi"],4)
    )
)
print(
    "The equivalence ratio, phi, such that the aluminium oxide is just starting to melt (Fuel Rich Case): phi = " + str(
        round(collection.find_one({"index":1})["phi"],4)
    )
)
'''
TASK 4
'''
print("TASK 4")
collection=db['q4']
print(
    "The equivalence ratio, phi, such that the aluminium oxide is fully melted (Fuel Lean Case): phi = " + str(
        round(collection.find_one({"index":0})["phi"],4)
    )
)
print(
    "The equivalence ratio, phi, such that the aluminium oxide is fully melted (Fuel Rich Case): phi = " + str(
        round(collection.find_one({"index":1})["phi"],4)
    )
)
'''
TASK 5
'''
print("TASK 5")
collection=db['q5']
print(
    "The Adiabatic Flame Temperature of the aluminium oxide, assuming the Al2O3 is liquid: AFT = " + str(
        round(collection.find_one({"index": 0})["AFT [K]"],2)
    )
)
'''
TASK 6
'''
print("TASK 6")
collection=db['q6']
print(
    "The Adiabatic Flame Temperature of the aluminium oxide, with an equivalence ratio of 1.5: AFT = " + str(
        round(collection.find_one({"index": 0})["AFT [K]"],2)
    )
)