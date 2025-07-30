from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import string
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load or generate encryption key
if not os.path.exists("secret.key"):
    with open("secret.key", "wb") as key_file:
        key_file.write(Fernet.generate_key())
with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

# Database Model
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_encrypted = db.Column(db.LargeBinary, nullable=False)

@app.route('/')
def index():
    return render_template("index3.html")

@app.route('/add', methods=['POST'])
def add_password():
    site = request.form['site']
    username = request.form['username']
    password = request.form['password']

    encrypted = fernet.encrypt(password.encode())
    new_entry = Password(site=site, username=username, password_encrypted=encrypted)
    db.session.add(new_entry)
    db.session.commit()
    return redirect('/')

@app.route('/retrieve', methods=['POST'])
def retrieve_password():
    site = request.form['site']
    entry = Password.query.filter_by(site=site).first()
    if entry:
        decrypted = fernet.decrypt(entry.password_encrypted).decode()
        return render_template("result.html", site=entry.site, username=entry.username, password=decrypted)
    return "No password found for this site."

@app.route('/generate')
def generate():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=12))
    return render_template("result.html", site="Generated", username="N/A", password=password)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=2000)
