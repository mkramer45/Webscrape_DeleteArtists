from flask import *
from functools import wraps
import sqlite3

artists = ['Solomun', 'Dubfire']

DATABASE = 'Beatscrape.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'my precious'

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')


@app.route('/scrapelist2', methods=['GET', 'POST'])
def enterArtistName():
	if request.method == 'POST':
		artists.append(request.form['ProducerName'])
	return render_template('scrapelist2.html', selected='submit', artists=artists)


def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('log'))
	return wrap


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect (url_for('log'))

@app.route('/hello')
@login_required
def hello():
	g.db = connect_db()
	cur = g.db.execute('select Artist, Song, Label, Price from BeatPortTechHouse')
	info = [dict(Artist=row[0], Song=row[1], Label=row[2], Price=row[3]) for row in cur.fetchall()]
	g.db.close()
	return render_template('hello.html', info=info)

@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True

			return redirect(url_for('hello'))
	return render_template('log.html', error=error)


@app.route('/delete_artist/<string:artist>', methods=['POST'])
def delete_artist(artist):
	g.db = connect_db()
	cur = g.db.execute("DELETE FROM BeatPortTechHouse, [artist]")
	g.db.commit()
	cur.close()
	flash('Artist Delete', 'success')
	return redirect(url_for('scrapelist2'))


if __name__ == '__main__':
	app.run(debug=True)