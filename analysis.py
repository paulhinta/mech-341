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