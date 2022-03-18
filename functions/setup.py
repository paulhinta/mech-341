from imp import cache_from_source
#This python scripts sets up a Mongo database with all of the data from the selected_data csv
#We do this because it's a lot faster to use Mongo than it is to read from a csv every time

import pandas                       #we will use pandas as the central tool to analyze this data
import pymongo                      #python + mongo
import certifi                      #to allow user certification when connecting to Mongo
from dotenv import load_dotenv      #loads secret environment variable (mongo password)
import os                           #fetches password from environment

load_dotenv()

pw = os.getenv("PASSWORD")          #fetch pw from environment

#mongo connection string
connect = "mongodb+srv://paulhinta:" + pw + "@cluster0.p3kas.mongodb.net/inputs?retryWrites=true&w=majority&ssl=true" 

ca = certifi.where()                #mongo connection certificate
client = pymongo.MongoClient(connect, tlsCAFile=ca)
db = client['inputs']               #database that we are using
collection=db['selected-data']      #connection that we are using

#read the input csv data
pd = pandas.read_csv("selected_data.csv")

#reset the index to iterate over as a dictionary (python dict == json)
pd.reset_index(inplace=True)
pd_dict=pd.to_dict("records")

#insert json data into database, now it's ready to use
collection.insert_many(pd_dict)