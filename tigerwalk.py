from flask import Flask
from flask import render_template, make_response, request
from flask_sqlalchemy import SQLAlchemy
from CASClient import CASClient

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = "tigerwalk key"
db = SQLAlchemy(app)

class users(db.Model):
    username = db.Column(db.String(150), nullable=False, primary_key=True) 
    name = db.Column(db.String(150), nullable=False) 
    phone = db.Column(db.Integer, nullable=True)
    groupme = db.Column(db.String(150), nullable=True) 
    facebook = db.Column(db.String(150), nullable=True) 
    profilepic = db.Column(db.Text(), nullable=True) 

    def __repr__(self):
        return f"shoeListing('{self.name}', '{self.phone}', '{self.groupme}', '{self.facebook}')"

@app.route('/')
def home():
    username = CASClient().authenticate()
    username = username.strip()
    
    html = render_template('home.html')
    response = make_response(html)
    return response

@app.route('/seewalkers')
def activeWalkers():
    html = render_template('activeWalkers.html')
    response = make_response(html)
    return response

@app.route('/myprofile')
def profile():
    html = render_template('activeWalkers.html')
    response = make_response(html)
    return response

if __name__ == '__main__':
    app.run(debug=True)