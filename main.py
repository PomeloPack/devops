from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
from config import config



#db connect
def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the postgres database ...')
        # **params copy all from database.ini into these two
        connection = psycopg2.connect(**params)

        #create a cursor
        cursor = connection.cursor()
        print('PostgreSQL database version: ')
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Ping was successful ... connection closed')
if __name__ == '__main__':
    connect()



#setup slack
app = Flask(__name__)

