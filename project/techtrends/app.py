import sqlite3
import logging
from datetime import datetime

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post
access_count = 0
def add_access_count():
    global access_count
    access_count = access_count + 1
    return access_count

# Function to get a count of posts 
def get_count_of_posts():
    connection = get_db_connection()
    postCount = connection.execute('SELECT Count(*) FROM posts').fetchone()
    connection.close()
    return postCount
    
#Function to get current time
def get_current_time():
    ct = datetime.now()
    dt_string = ct.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 

@app.route('/')

def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()    
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    add_access_count()
    if post is None:
      app.logger.info(get_current_time() +' A non-existing article is accessed and a 404 page is returned')        
      return render_template('404.html'), 404
    else:
      
      app.logger.info(get_current_time() + ' Article ' + post["title"] + ' retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info(get_current_time() +' About us page is retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        

        if not title:
            flash('Title is required!')
        else:
            app.logger.info(get_current_time() +' New article is created with title :' + title)
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info(get_current_time() +' Healthz request successfull')
    return response

@app.route('/metrics')
def metrics():
                   
            postCount = get_count_of_posts()
            response = app.response_class(
            response=json.dumps({"db_connection_count":access_count,"post_count":postCount[0]}),
            status=200,
            mimetype='application/json'
            )
            app.logger.info(get_current_time() +' Metrics request successfull : db_connection_count ' + str(access_count) + ' post_count ' + str(postCount[0]))
            return response
            
# start the application on port 3111
if __name__ == "__main__":
# Stream logs to a file, and set the default log level to DEBUG
   logging.basicConfig(level=logging.DEBUG)
   app.run(host='0.0.0.0', port='3111')
   

