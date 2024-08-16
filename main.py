from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
from config import config
import logging


# Import your models
from db_models import User, Task, Project, Comment


#setup slack
app = Flask(__name__)

# logs
logging.basicConfig(format='%(asctime)s - %(levelname)s -  %(message)s', level=logging.DEBUG)

logger = logging.getLogger('basic_log')
formatter_base = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')



#db connect
def db_connect():
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
    db_connect()


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        else:
            due_date = None
        new_task = Task(title=title, description=description, due_date=due_date)
        db_connect.session.add(new_task)
        db_connect.session.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db_connect.session.delete(task)
    db_connect.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)


