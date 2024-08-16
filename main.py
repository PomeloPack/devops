from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

#connect to database
connection = psycopg2.connect(host='localhost', port='5432', database='task_manager', user='postgres', password='57Baf1a8?')



#setup slack
app = Flask(__name__)

