import sqlite3
import json
from flask import Flask, render_template, g, request
app = Flask(__name__, static_url_path='/static')

DATABASE = '/var/www/nbcapp/nbcapp/oddmanout.db'


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


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


@app.route('/oddmanout-query')
def oddmanout_test():
    group = request.args.get('group')
    cur = get_db().cursor()
    cur.execute('select * from oddmanout where "group"=' + group + '\
                order by random() limit 1')
    rows = cur.fetchall()
    if len(rows) == 0:
        res = 'na'
    else:
        res = make_dicts(cur, rows[0])
    cur.close()
    return json.dumps(res)


if __name__ == '__main__':
    app.run()
