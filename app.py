import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
db_password = os.getenv('DB_PASSWORD')
if not db_password:
    raise ValueError("DB_PASSWORD is not set in the environment variables.")

connection_string = f"mongodb+srv://grahamd:{
    db_password}@cluster0.dxb95.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
