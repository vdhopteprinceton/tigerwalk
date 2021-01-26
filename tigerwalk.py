from flask import Flask
from flask import render_template, make_response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = "tigerwalk key"
# db = SQLAlchemy(app)

# class shoeListing(db.Model):
#     name = db.Column(db.String(150), nullable=False, primary_key=True)
#     retail = db.Column(db.Integer, nullable=True)
#     resale = db.Column(db.Integer, nullable=True)
#     profit = db.Column(db.Integer, nullable=True)
#     image = db.Column(db.Text, nullable=True)
#     month = db.Column(db.String(10), nullable=False)
#     date = db.Column(db.Integer, nullable=True)

#     def __repr__(self):
#         return f"shoeListing('{self.name}', '{self.retail}', '{self.resale}', '{self.date}')"

@app.route('/')
def home():
    html = render_template('home.html')
    response = make_response(html)
    return response

if __name__ == '__main__':
    app.run(debug=True)