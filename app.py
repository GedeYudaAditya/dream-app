from flask import Flask, render_template, request, session, redirect, url_for
# import pyodbc
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "rahasiabangetdeh"


# def connection():
#     conn = pyodbc.connect(
#         driver='{SQL Server}',
#         server='localhost,3306',
#         database='dream-app',
#         uid='root',
#         pwd=''
#     )

#     return conn


@app.route('/')
def index():
    # conn = connection()
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM users')

    if 'email' not in session:
        return redirect(url_for('login'))

    title = 'Home'

    # model logic

    return render_template('index.html', title=title)


@app.route('/setting')
def setting():
    if 'email' not in session:
        return redirect(url_for('login'))

    title = 'Setting'

    return render_template('setting.html', title=title)


@app.route('/login')
def login():
    if 'email' in session:
        return redirect(url_for('index'))

    title = 'Login'

    return render_template('login.html', title=title)


@app.route('/login', methods=['POST'])
def loginProses():

    if 'email' in session:
        return redirect(url_for('index'))

    email = request.form['email']
    password = request.form['password']

    response = requests.post('https://reqres.in/api/login',
                             json={'email': email, 'password': password})

    if response.status_code == 200:
        session['email'] = email
        session['token'] = response.json()['token']

        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/register')
def register():
    if 'email' in session:
        return redirect(url_for('index'))

    title = 'Register'

    return render_template('register.html', title=title)


@app.route('/register', methods=['POST'])
def registerProses():
    if 'email' in session:
        return redirect(url_for('index'))

    nama = request.form['nama']
    email = request.form['email']
    password = request.form['password']

    if nama == '' or email == '' or password == '':
        return redirect(url_for('register'))
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():

    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    session.pop('token', None)

    return redirect(url_for('index'))

# parsing nilai int


# @app.route('/parsing/<int:angka>')
# def parsing(angka):
    # return 'Angka yang anda masukkan adalah : {}'.format(angka)

# argument parsee


# @app.route('/argument')
# def argument():
    # data = request.args.get('nilai')
    # return 'Nilai yang anda masukkan adalah : {}'.format(data)

# parsing nilai string ke session


# @app.route('/session/<string:nama>')
# def sessionSet(nama):
#     session["nama"] = nama
#     return render_template('session_set.html', nama=nama)


# @app.route('/session_show')
# def sessionShow():
#     try:
#         nama = session["nama"]
#         return render_template('session.html', nama=nama)
#     except KeyError:
#         return render_template('error.html')
# @app.route('/logout')
# def logout():
#     session.pop('nama', None)
#     return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
