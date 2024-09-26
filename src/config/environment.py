from re import L
from dotenv import load_dotenv
import os

load_dotenv()

CLOUD_DATABASE = os.getenv('CLOUD_DATABASE')
LOCAL_DATABASE = os.getenv('LOCAL_DATABASE')
