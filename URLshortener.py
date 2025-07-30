from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, flash 
import random
import string 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///urlshortener.db"
db = SQLAlchemy(app) 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

class Urlshortener(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    longurl = db.Column(db.String(200), unique=True, nullable=False)  
    shorturl = db.Column(db.String(200), unique=True, nullable=False)  
 

    def __repr__(self):
        return f"{self.shorturl}" 
    
# Generate short code
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Home page
@app.route("/")
def home():
    return render_template("index1.html")    

@app.route("/shorten", methods=["POST"])
def shorten_url():
    long_url = request.form['longUrl']    

    existing = Urlshortener.query.filter_by(longurl=long_url).first()
    if existing:
       return render_template("index1.html", short_url=existing.shorturl)  
 
    while True:
        short_url = generate_short_url()
        if not Urlshortener.query.filter_by(shorturl=short_url).first():
            break

    new_url = Urlshortener(longurl=long_url, shorturl=short_url)
    db.session.add(new_url)
    db.session.commit()

    return render_template("index1.html", short_url=short_url)

# Redirect to long URL
@app.route("/<shorturl>")
def redirect_to_url(shorturl):
    result = Urlshortener.query.filter_by(shorturl=shorturl).first()
    if result:
        return redirect(result.longurl)
    else:
        return "URL not found", 404


if __name__ == "__main__" :

    with app.app_context():
        db.create_all()

    app.run(debug = True , port = 1000)  
