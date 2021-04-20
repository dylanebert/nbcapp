import sqlite3
from flask import Flask, render_template, g
app = Flask(__name__, static_url_path='/static')

DATABASE = 'oddmanout.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/actions')
def actions():
	return render_template('actions.html')

@app.route('/oddmanout')
def oddmanout():
	return render_template('oddmanout.html')

@app.route('/oddmanout-test')
def oddmanout_test():
	cur = get_db().cursor()
	cur.execute('select * from oddmanout')
	print(cur.fetchall())
	cur.close()
	return 'success'

if __name__ == '__main__':
	app.run()
