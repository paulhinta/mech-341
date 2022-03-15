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
plt.show()
'''
TASK 2
'''
print("TASK 2")
collection=db['q2']
#Fetch q2 data from the database
print(
    "Considering the oxidation of aluminium with water, the equivalence ratio,phi, so that the produced water is saturated vapour is: phi = " + str(
        round(collection.find_one({"index":0})["Equivalence Ratio"],4)
    )
    + "\nThis occurs at a temperature, T: T = " + str(
        round(collection.find_one({"index":1})["Temperature [K]"],2)
    )
)
print("\n")
'''
TASK 3
'''
print("TASK 3")
collection=db['q3']
print(
    "The equivalence ratio, phi, such that the aluminium oxide is just starting to melt: phi = " + str(
        round(collection.find_one({"index":0})["phi"],4)
    )
)
print("\n")
'''
TASK 4
'''