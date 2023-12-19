import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

mysql = MySQL(app)

# Create a table for the tasks

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tasks (description) VALUES (%s)', (description,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE tasks SET completed = 1 WHERE id = %s', (task_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)