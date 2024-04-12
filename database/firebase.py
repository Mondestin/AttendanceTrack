import pyrebase
import json
import firebase_admin
from firebase_admin import credentials
#from dotenv import dotenv_values
import os
from dotenv import load_dotenv

load_dotenv()
# get variables from .example.env file
#config = dotenv_values(".example.env")

firebase_service_account_key = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")

cred = credentials.Certificate(json.loads(firebase_service_account_key, strict=False))
firebase_admin.initialize_app(cred)
# load firebase config
firebase = pyrebase.initialize_app(json.loads(os.getenv("FIREBASE_CONFIG"), strict=False))
# init firebase as db
db = firebase.database()
# init firebase as authSession
authSession = firebase.auth()